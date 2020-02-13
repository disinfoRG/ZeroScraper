from selenium import webdriver
import requests
from newsSpiders import helpers
from newsSpiders.types import SiteConfig
import pugsql
import os
import json
import time
from random import uniform
import argparse

queries = pugsql.module("./queries")
queries.connect(os.getenv("DB_URL"))


# feat: discover, update article by url
def get_article_by_request(url, user_agent):
    headers = {"User-Agent": user_agent}
    r = requests.get(url, headers=headers)

    return r.text


def get_article_by_selenium(url, user_agent):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--proxy-server={}".format(os.getenv("PROXY_URL")))
    options.headless = True

    driver = webdriver.Chrome(os.getenv("CHROMEDRIVER_BIN"), options=options)
    driver.get(url)
    time.sleep(uniform(3, 5))

    return driver.page_source


def get_dcard_article(url, user_agent):
    result = dict()
    headers = {"User-Agent": user_agent}
    post_id = url.split("/p/")[-1]
    post_api = f"https://www.dcard.tw/_api/posts/{post_id}"
    post_r = requests.get(post_api, headers=headers)
    result["post"] = post_r.json()

    comment_api = f"https://www.dcard.tw/_api/posts/{post_id}/comments?limit=100"
    comment_r = requests.get(comment_api, headers=headers)
    result["comments"] = comment_r.json()

    return json.dumps(result)


def update_article_table(article_info, site_info, crawl_time):
    next_snapshot_at = article_info
    article_id = article_info["article_id"]
    snapshot_count = article_info["snapshot_count"]
    site_type = site_info["type"]

    if next_snapshot_at != 0:
        next_snapshot_at = helpers.generate_next_fetch_time(site_type, 1, crawl_time)
    queries.update_article_snapshot_time(
        article_id=article_id,
        crawl_time=crawl_time,
        snapshot_count=snapshot_count + 1,
        next_snapshot_at=next_snapshot_at,
    )


def update(article_id):
    # read url from article_id
    article_info = queries.get_article_by_id(article_id=article_id)
    print(article_info)

    # crawler config (ua, selenium) from site
    site_info = queries.get_site_by_id(site_id=article_info["site_id"])
    site_config = json.loads(site_info["config"])
    crawler_config = SiteConfig.default()
    crawler_config.update(site_config)
    user_agent = crawler_config["ua"]
    use_selenium = crawler_config.get("selenium", args.selenium)

    # get html
    crawl_time = int(time.time())
    if "dcard" in article_info["url"]:
        snapshot = get_dcard_article(article_info["url"], user_agent)
    elif use_selenium:
        snapshot = get_article_by_selenium(article_info["url"], user_agent)
    else:
        snapshot = get_article_by_request(article_info["url"], user_agent)

    # update article table: last_snapshot_at, snapshot_count
    update_article_table(article_info, site_info, crawl_time)

    # add article snapshot
    queries.insert_snapshot(
        article_id=article_info["article_id"], crawl_time=crawl_time, raw_data=snapshot
    )


def main(args):
    if args.command == "update":
        update(args.id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title="sub command", dest="command", required=True)

    update_cmd = cmds.add_parser("update", help="do update")
    update_cmd.add_argument(
        "id", type=int, help="id of the site to update in news db", nargs="?"
    )
    update_cmd.add_argument(
        "--selenium", help="use selenium to update", action="store_true"
    )

    args = parser.parse_args()
    main(args)

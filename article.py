#!/usr/bin/env python3

from selenium import webdriver
import requests
from url_normalize import url_normalize
import pugsql
import os
import json
import time
from random import uniform
import argparse
import zlib
from newsSpiders import helpers
from newsSpiders.types import SiteConfig


queries = pugsql.module("./queries")
queries.connect(os.getenv("DB_URL"))


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
        next_snapshot_at = helpers.generate_next_fetch_time(
            site_type, fetch_count=1, snapshot_time=crawl_time
        )
    queries.update_article_snapshot_time(
        article_id=article_id,
        last_snapshot_at=crawl_time,
        snapshot_count=snapshot_count + 1,
        next_snapshot_at=next_snapshot_at,
    )


def update(args):
    print(args.selenium)
    # read url from article_id
    article_info = queries.get_article_by_id(article_id=args.id)
    print(article_info)

    # crawler config (ua, selenium) from site
    site_info = queries.get_site_by_id(site_id=article_info["site_id"])
    site_config = json.loads(site_info["config"])
    crawler_config = SiteConfig.default()
    crawler_config.update(site_config)
    # todo: command line argument should take precedence than config
    user_agent = crawler_config["ua"]
    use_selenium = crawler_config.get("selenium", args.selenium)
    print(use_selenium)
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
        article_id=article_info["article_id"], snapshot_at=crawl_time, raw_data=snapshot
    )


def discover(args):
    # check if args.url exists in db, if so, print message and exist.
    url = url_normalize(args.url)
    exist = queries.check_article_existence(url=url)["exist"]
    if exist == 1:
        article_id = queries.get_article_by_url(url=url)["article_id"]
        print(f"The given url exists in the database, having article_id {article_id}.")
        print(f"Please do update instead.")
        return article_id

    crawler_config = SiteConfig.default()
    user_agent = crawler_config["ua"]
    crawl_time = int(time.time())
    if "dcard" in args.url:
        snapshot = get_dcard_article(args.url, user_agent)
    elif args.selenium:
        snapshot = get_article_by_selenium(args.url, user_agent)
    else:
        snapshot = get_article_by_request(args.url, user_agent)

    article_type = helpers.get_article_type(args.url)
    url_hash = zlib.crc32(args.url.encode())
    site_type = helpers.get_site_type(queries, args.site_id)
    next_snapshot_at = (
        0
        if site_type is None
        else helpers.generate_next_fetch_time(
            site_type, fetch_count=1, snapshot_time=crawl_time
        )
    )
    inserted_article_id = queries.insert_article(
        site_id=args.site_id,
        url=args.url,
        url_hash=url_hash,
        first_snapshot_at=crawl_time,
        last_snapshot_at=crawl_time,
        next_snapshot_at=next_snapshot_at,
        snapshot_count=1,
        redirect_to=None,
        article_type=article_type,
    )

    queries.insert_snapshot(
        article_id=inserted_article_id, snapshot_at=crawl_time, raw_data=snapshot
    )
    print(f"Finish discover, new article_id = {inserted_article_id}")
    return inserted_article_id


def main(args):
    if args.command == "update":
        update(args)
    elif args.command == "discover":
        discover(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title="sub command", dest="command", required=True)

    discover_cmd = cmds.add_parser("discover", help="do discover")
    discover_cmd.add_argument(
        "url",
        type=str,
        help="url of the article to be snapshot first-time in the db.",
        nargs="?",
    )
    discover_cmd.add_argument(
        "--selenium", help="use selenium to load website", action="store_true"
    )
    discover_cmd.add_argument(
        "--site-id",
        help="the site id that this article belongs to. optional.",
        type=int,
        default=0,
    )

    update_cmd = cmds.add_parser("update", help="do update")
    update_cmd.add_argument(
        "id", type=int, help="id of the article to update in news db", nargs="?"
    )
    update_cmd.add_argument(
        "--selenium", help="use selenium to load website", action="store_true"
    )

    args = parser.parse_args()
    main(args)

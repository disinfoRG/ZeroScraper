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
import logging
from newsSpiders import helpers
from newsSpiders.types import SiteConfig

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s %(filename)s %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.getenv("LOG_LEVEL", "INFO"),
)

logger = logging.getLogger(__name__)

queries = pugsql.module("./queries")
queries.connect(os.getenv("DB_URL"))


def get_article_by_request(url, user_agent, **kwargs):
    headers = {"User-Agent": user_agent}
    r = requests.get(url, headers=headers, **kwargs)

    return r.text


def get_article_by_selenium(url, user_agent):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")
    options.headless = True
    proxy_url = os.getenv("PROXY_URL")
    if proxy_url:
        options.add_argument("--proxy-server={}".format(os.getenv("PROXY_URL")))

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

    comment_api = f"{post_api}/comments?limit=100"
    comment_r = requests.get(comment_api, headers=headers)
    result["comments"] = comment_r.json()

    return json.dumps(result)


def update_article_table(article_info, site_info, crawl_time):
    next_snapshot_at = article_info
    article_id = article_info["article_id"]
    snapshot_count = article_info["snapshot_count"]

    if next_snapshot_at != 0:
        next_snapshot_at = helpers.generate_next_snapshot_time(
            site_info["url"], snapshot_count=1, snapshot_time=crawl_time
        )
    queries.update_article_snapshot_time(
        article_id=article_id,
        last_snapshot_at=crawl_time,
        snapshot_count=snapshot_count + 1,
        next_snapshot_at=next_snapshot_at,
    )


def update(args):
    # read url from article_id
    article_info = queries.get_article_by_id(article_id=args.id)

    # crawler config (ua, selenium) from site
    site_info = queries.get_site_by_id(site_id=article_info["site_id"])
    site_config = json.loads(site_info["config"])
    crawler_config = SiteConfig.default()
    crawler_config.update(site_config)

    user_agent = args.ua or crawler_config["ua"]
    use_selenium = args.selenium or crawler_config["selenium"]
    # get html
    now = int(time.time())
    if "dcard" in article_info["url"]:
        snapshot = get_dcard_article(article_info["url"], user_agent)
    elif use_selenium:
        snapshot = get_article_by_selenium(article_info["url"], user_agent)
    elif "ptt" in args.url:
        snapshot = get_article_by_request(args.url, user_agent, cookies={"over18": "1"})
    else:
        snapshot = get_article_by_request(article_info["url"], user_agent)

    # update article table: last_snapshot_at, snapshot_count
    update_article_table(article_info, site_info, now)

    # add article snapshot
    queries.insert_snapshot(
        article_id=article_info["article_id"], snapshot_at=now, raw_data=snapshot
    )


def discover(args):
    # check if args.url exists in db, if so, print message and exist.
    url = url_normalize(args.url)
    url_hash = str(zlib.crc32(url.encode()))
    result = queries.get_article_id_by_url(url=url, url_hash=url_hash)
    if result is not None:
        logger.info(
            f"URL exists in the database, with article_id {result['article_id']}. Please do update instead"
        )
        return

    crawler_config = SiteConfig.default()
    user_agent = args.ua or crawler_config["ua"]
    now = int(time.time())
    if "dcard" in args.url:
        snapshot = get_dcard_article(args.url, user_agent)
    elif "ptt" in args.url:
        snapshot = get_article_by_request(args.url, user_agent, cookies={"over18": "1"})
    elif args.selenium:
        snapshot = get_article_by_selenium(args.url, user_agent)
    else:
        snapshot = get_article_by_request(args.url, user_agent)

    article_type = helpers.get_article_type(args.url)
    url_hash = zlib.crc32(args.url.encode())
    if args.site_id:
        site_info = queries.get_site_by_id(site_id=args.site_id)
    else:
        site_info = None

    next_snapshot_at = (
        0
        if site_info is None
        else helpers.generate_next_snapshot_time(
            site_info["url"], snapshot_count=1, snapshot_time=now
        )
    )

    inserted_article_id = queries.insert_article(
        site_id=args.site_id,
        url=args.url,
        url_hash=url_hash,
        first_snapshot_at=now,
        last_snapshot_at=now,
        next_snapshot_at=next_snapshot_at,
        snapshot_count=1,
        redirect_to=None,
        article_type=article_type,
    )

    queries.insert_snapshot(
        article_id=inserted_article_id, snapshot_at=now, raw_data=snapshot
    )
    logger.info(f"Finish discover {args.url}, new article_id = {inserted_article_id}")
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
    discover_cmd.add_argument("--ua", type=str, help="user agent string", nargs="?")
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
    update_cmd.add_argument("--ua", type=str, help="user agent string", nargs="?")
    update_cmd.add_argument(
        "--selenium", help="use selenium to load website", action="store_true"
    )

    args = parser.parse_args()
    main(args)

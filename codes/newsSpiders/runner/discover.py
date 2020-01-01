import os
import sqlalchemy as db
from helpers import connect_to_db


def run(site_id, args, defaults):
    _, connection, tables = connect_to_db()
    site = tables["Site"]

    query = db.select([site.columns.url, site.columns.type, site.columns.config]).where(
        site.columns.site_id == site_id
    )
    site_info = dict(connection.execute(query).fetchone())
    site_url = site_info["url"]
    site_type = site_info["type"]
    article_pattern = site_info["config"]["article"]
    following_pattern = site_info["config"].get("following", "")
    if args.depth is not None:
        depth = args.depth
    else:
        depth = site_info["config"].get("depth", defaults["depth"])

    if args.delay is not None:
        delay = args.delay
    else:
        delay = site_info["config"].get("delay", defaults["delay"])
    if args.ua is not None:
        site_ua = args.ua
    else:
        site_ua = site_info["config"].get("ua", defaults["ua"])
    if args.selenium is not None:
        selenium = args.selenium
    else:
        selenium = site_info["config"].get("selenium", False)

    os.system(
        f"scrapy crawl discover_new_articles \
                -a site_id='{site_id}' \
                -a site_url='{site_url}' \
                -a site_type='{site_type}' \
                -a article_url_patterns='{article_pattern}' \
                -a following_url_patterns='{following_pattern}' \
                -a selenium='{selenium}' \
                -s DEPTH_LIMIT={depth} \
                -s DOWNLOAD_DELAY={delay} \
                -s USER_AGENT='{site_ua}'"
    )

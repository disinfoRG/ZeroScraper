import argparse
import os
import sqlalchemy as db
from helpers import connect_to_db


parser = argparse.ArgumentParser()
parser.add_argument("--site_id", help="site id to crawl")
parser.add_argument(
    "--depth", help="desired depth limit; 0 if no limit imposed.", type=int
)
parser.add_argument("--delay", help="time delayed for request.")
parser.add_argument("--ua", help="user_agent")
parser.add_argument(
    "-d",
    "--discover",
    action="store_true",
    help="execute spider to discover new articles",
)
parser.add_argument(
    "-u", "--update", action="store_true", help="execute spider to update articles"
)

# set up
args = parser.parse_args()
root_dir = os.getcwd().split("/NewsScraping/")[0] + "/NewsScraping"
engine, connection, tables = connect_to_db()
site = tables["Site"]
DEFAULT_DEPTH = 0
DEFAULT_DELAY = 1.5
DEFAULT_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
# execute
if args.discover:
    args.site_id = int(args.site_id)
    query = db.select([site.columns.url, site.columns.type, site.columns.config]).where(
        site.columns.site_id == args.site_id
    )
    site_info = dict(connection.execute(query).fetchone())
    site_url = site_info["url"]
    site_type = site_info["type"]
    article_pattern = site_info["config"]["article"]
    following_pattern = site_info["config"].get("following", "")
    if args.depth is not None:
        depth = args.depth
    else:
        depth = site_info["config"].get("depth", DEFAULT_DEPTH)

    if args.delay is not None:
        delay = args.delay
    else:
        delay = site_info["config"].get("delay", DEFAULT_DELAY)
    if args.ua is not None:
        site_ua = args.ua
    else:
        site_ua = site_info["config"].get("user_agent", DEFAULT_UA)

    os.system(
        f"scrapy crawl discover_new_articles \
                -a site_id='{args.site_id}' \
                -a site_url='{site_url}' \
                -a site_type='{site_type}' \
                -a article_url_patterns='{article_pattern}' \
                -a following_url_patterns='{following_pattern}' \
                -s DEPTH_LIMIT={depth} \
                -s DOWNLOAD_DELAY={delay} \
                -s USER_AGENT='{site_ua}'"
    )

elif args.update:
    if args.delay is not None:
        delay = args.delay
    else:
        delay = DEFAULT_DELAY
    if args.ua is not None:
        ua = args.ua
    else:
        ua = DEFAULT_UA
    os.system(
        f"scrapy crawl update_contents \
                -s DOWNLOAD_DELAY={delay} \
                -s USER_AGENT='{ua}'"
    )
else:
    raise Exception(
        "Please specify action by adding either --discover or --update flag"
    )

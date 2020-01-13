import os
import argparse
import time
import pugsql
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newsSpiders.crawler import discover, update

queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))

parser = argparse.ArgumentParser()
parser.add_argument("--site_id", type=int, help="site id to crawl")
parser.add_argument(
    "--depth", help="desired depth limit; 0 if no limit imposed.", type=int
)
parser.add_argument("--delay", help="time delayed for request.")
parser.add_argument("--ua", help="user_agent")
parser.add_argument("--selenium", help="use selenium to load website or not.")
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

# execute
process = CrawlerProcess(get_project_settings())
if args.discover:
    crawl_time = int(time.time())
    queries.update_site_crawl_time(site_id=args.site_id, crawl_time=crawl_time)
    discover.create(process, queries, args.site_id, vars(args))
elif args.update:
    update.create(process, vars(args))
else:
    raise Exception(
        "Please specify action by adding either --discover or --update flag"
    )
process.start()

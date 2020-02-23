import os
import argparse
import time
import pugsql
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from newsSpiders.runner import discover, update
from newsSpiders.process import pid_lock, Cleanup

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
parser.add_argument("--limit-sec", type=int, help="time limit to run in seconds")

# set up

with pid_lock(queries, "execute_spider"):
    args = parser.parse_args()
    runner = CrawlerRunner(get_project_settings())
    if args.discover:
        crawl_time = int(time.time())
        queries.update_site_crawl_time(site_id=args.site_id, crawl_time=crawl_time)
        discover.run(runner, args.site_id, vars(args))
    elif args.update:
        if args.site_id:
            print(f"Update for site {args.site_id}.")
        else:
            print(f"Update all.")
        update.run(runner, args.site_id, vars(args))
    else:
        raise Exception(
            "Please specify action by adding either --discover or --update flag"
        )
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    if args.limit_sec is not None:
        reactor.callLater(args.limit_sec, Cleanup(runner).terminate)

    reactor.run()

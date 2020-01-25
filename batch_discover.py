from dotenv import load_dotenv

load_dotenv()

import os
import argparse
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import newsSpiders.runner.discover
import pugsql


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit-sec", type=int, help="time limit to run in seconds")
    return parser.parse_args()


def terminate():
    reactor.stop()


def main():
    args = parse_args()

    queries = pugsql.module("queries/")
    queries.connect(os.getenv("DB_URL"))

    sites = queries.get_sites_to_crawl()

    configure_logging()
    runner = CrawlerRunner(get_project_settings())
    for site in sites:
        newsSpiders.runner.discover.run(runner, site["site_id"])
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    if args.limit_sec is not None:
        reactor.callLater(args.limit_sec, terminate)
    reactor.run()


if __name__ == "__main__":
    main()

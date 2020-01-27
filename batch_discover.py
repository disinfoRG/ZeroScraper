from dotenv import load_dotenv

load_dotenv()

import os
import sys
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
    parser.add_argument(
        "--pid-name", default="discover", help="variable name to store PID"
    )
    return parser.parse_args()


class Cleanup:
    def __init__(self, runner):
        self.runner = runner

    def terminate(self):
        self.runner.stop()


class ProcessError(Exception):
    pass


class PIDLock:
    def __init__(self, queries, proc_name):
        self.queries = queries
        self.key = f"{proc_name}:pid"

    def __enter__(self):
        variable = self.queries.get_variable(key=self.key)
        if variable is not None and variable["value"]:
            raise ProcessError("Another discover process already running.")
        self.queries.set_variable(key=self.key, value=str(os.getpid()))

    def __exit__(self, type_, value, traceback):
        self.queries.delete_variable(key=self.key)


def pid_lock(queries, proc_name):
    return PIDLock(queries, proc_name)


def main():
    args = parse_args()

    queries = pugsql.module("queries/")
    queries.connect(os.getenv("DB_URL"))

    with pid_lock(queries, args.pid_name):
        sites = queries.get_sites_to_crawl()

        configure_logging()
        runner = CrawlerRunner(get_project_settings())
        for site in sites:
            newsSpiders.runner.discover.run(runner, site["site_id"])
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

        if args.limit_sec is not None:
            reactor.callLater(args.limit_sec, Cleanup(runner).terminate)

        reactor.run()


if __name__ == "__main__":
    main()

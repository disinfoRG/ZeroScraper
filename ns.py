#!/usr/bin/env python3

from dotenv import load_dotenv

load_dotenv()

import os
import logging

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.getenv("LOG_LEVEL", "INFO"),
)
logger = logging.getLogger(__name__)

import argparse
import pugsql
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import newsSpiders.runner.discover
import newsSpiders.runner.update


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
        self.proc_name = proc_name

    def __enter__(self):
        with self.queries.transaction():
            lock = self.queries.get_variable(key=self.key)
            if lock is not None and lock["value"]:
                raise ProcessError(f"Another {self.proc_name} process already running.")
            self.queries.set_variable(key=self.key, value=str(os.getpid()))

    def __exit__(self, type_, value, traceback):
        self.queries.delete_variable(key=self.key)


def pid_lock(queries, proc_name):
    return PIDLock(queries, proc_name)


def discover(args):
    queries = pugsql.module("queries/")
    queries.connect(os.getenv("DB_URL"))

    with pid_lock(queries, args.proc_name):
        sites = list(queries.get_sites_to_crawl())
        if len(sites) == 0:
            logger.info("No sites found.  Quit.")
            return

        configure_logging()
        runner = CrawlerRunner(get_project_settings())
        for site in sites:
            newsSpiders.runner.discover.run(runner, site["site_id"], vars(args))
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

        if args.limit_sec is not None:
            reactor.callLater(args.limit_sec, Cleanup(runner).terminate)

        reactor.run()

    queries.disconnect()


def update(args):
    queries = pugsql.module("queries/")
    queries.connect(os.getenv("DB_URL"))

    with pid_lock(queries, args.proc_name):
        sites = list(queries.get_sites_to_crawl())
        if len(sites) == 0:
            logger.info("No sites found.  Quit.")
            return

        configure_logging()
        runner = CrawlerRunner(get_project_settings())
        for site in sites:
            newsSpiders.runner.update.run(runner, site["site_id"])
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

        if args.limit_sec is not None:
            reactor.callLater(args.limit_sec, Cleanup(runner).terminate)

        reactor.run()

    queries.disconnect()


def main(args):
    if args.command == "discover":
        discover(args)
    elif args.command == "update":
        update(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title="sub command", dest="command", required=True)

    discover_cmd = cmds.add_parser("discover", help="do discover")
    discover_cmd.add_argument(
        "--limit-sec", type=int, help="time limit to run in seconds"
    )
    discover_cmd.add_argument(
        "--proc-name", default="discover", help="process name to store PID"
    )
    discover_cmd.add_argument(
        "--dedup-limit",
        help="number of recent articles url to store in memory",
        type=int,
    )
    update_cmd = cmds.add_parser("update", help="do update")
    update_cmd.add_argument(
        "--limit-sec", type=int, help="time limit to run in seconds"
    )
    update_cmd.add_argument(
        "--proc-name", default="update", help="process name to store PID"
    )

    args = parser.parse_args()
    main(args)

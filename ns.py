#!/usr/bin/env python3

from dotenv import load_dotenv

load_dotenv()

import os
from getpass import getpass
import logging

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.getenv("LOG_LEVEL", "INFO"),
)
logger = logging.getLogger(__name__)

import argparse
import pugsql
import json
import requests
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
        sites = queries.get_sites_to_crawl()

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
        sites = queries.get_sites_to_crawl()

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


def login():
    username = input("username: ")
    password = getpass("password: ")
    user_credential = {"username": username, "password": password}

    r = requests.post(os.getenv("API_URL") + "/login", json=user_credential)
    if r.status_code == 200:
        logger.info("Login successful. ")
        json.dump(r.json(), open("secrets.json", "w"))
    else:
        logger.info(f"Login failed. Message: {r.json()['message']}")


def stats(args):
    try:
        access_token = json.load(open("secrets.json"))["access_token"]
    except FileNotFoundError:
        logger.error("File secrets.json is missing. Please login first.")
        return
    else:
        logger.debug("Found login credential.")
        if args.site_id:
            r = requests.get(f'{os.getenv("API_URL")}/stats?site_id={args.site_id}',
                             cookies={'access_token_cookie': access_token})
        elif args.date:
            r = requests.get(f'{os.getenv("API_URL")}/stats?date={args.date}',
                             cookies={'access_token_cookie': access_token})
        else:
            r = requests.get(f'{os.getenv("API_URL")}/stats',
                             cookies={'access_token_cookie': access_token})
        ## todo: what's an ideal way to return the result. using return doesn't seem ideal as a command-line tool.

        return r.json()


def main(args):
    if args.command == "discover":
        discover(args)
    elif args.command == "update":
        update(args)
    elif args.command == "login":
        login()
    elif args.command == "stats":
        stats(args)


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

    login_cmd = cmds.add_parser("login", help="log in to api")

    stats_cmd = cmds.add_parser("stats", help="get stats from api")
    stats_cmd.add_argument(
        "--site-id", type=int, help="retrieve stats of a particular site", nargs="?"
    )
    stats_cmd.add_argument(
        "--date", type=str, help="retrieve stats of a particular date"
    )

    args = parser.parse_args()
    main(args)

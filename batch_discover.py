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
    parser.add_argument("--pid-file", help="path to file to store PID")
    return parser.parse_args()


class Cleanup:
    def __init__(self, runner):
        self.runner = runner

    def terminate(self):
        self.runner.stop()


class PIDLock:
    def __init__(self, path):
        self.path = path

    def lock(self):
        if self.path:
            if os.path.exists(self.path):
                raise Exception("Another discover process already running.")
            with open(self.path, "w") as f:
                f.write(str(os.getpid()))

    def unlock(self):
        if self.path is not None:
            os.remove(self.path)


def main():
    args = parse_args()

    pid_lock = PIDLock(args.pid_file)
    try:
        pid_lock.lock()
    except Exception:
        sys.stderr.write("Another discover process already running.  Exit.")
        sys.exit(-1)

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
        reactor.callLater(args.limit_sec, Cleanup(runner).terminate)

    reactor.run()

    pid_lock.unlock()


if __name__ == "__main__":
    main()

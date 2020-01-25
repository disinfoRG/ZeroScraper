from dotenv import load_dotenv

load_dotenv()

import os
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import newsSpiders.runner.discover
import pugsql


def main():
    queries = pugsql.module("queries/")
    queries.connect(os.getenv("DB_URL"))

    sites = queries.get_sites_to_crawl()

    configure_logging()
    runner = CrawlerRunner(get_project_settings())
    for site in sites:
        newsSpiders.runner.discover.run(runner, site["site_id"])
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


if __name__ == "__main__":
    main()

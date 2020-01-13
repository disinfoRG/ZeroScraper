from dotenv import load_dotenv

load_dotenv()

import os
import sys
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import newsSpiders.crawler.discover
import pugsql

queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))

sites = sorted(
    queries.get_sites_to_crawl(),
    key=lambda k: 0 if k["last_crawl_at"] is None else k["last_crawl_at"],
)

if len(sites) == 0:
    sys.exit(0)

configure_logging()
runner = CrawlerRunner(get_project_settings())
for site in sites:
    newsSpiders.crawler.discover.create(runner, queries, site["site_id"])
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()

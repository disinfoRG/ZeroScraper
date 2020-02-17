import time
import os
import pugsql
import json
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from newsSpiders.types import SiteConfig
from newsSpiders.helpers import connect_to_db
from newsSpiders.spiders.update_contents_spider import UpdateContentsSpider
from newsSpiders.spiders.update_dcard_spider import UpdateDcardPostsSpider

queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))


def get_articles_to_update(site_id, current_time):
    if site_id:
        return queries.get_articles_to_update(
            site_id=site_id, current_time=current_time
        )
    else:
        return queries.get_all_articles_to_update(current_time=current_time)


def run(runner, site_id, args=None):
    site_conf = SiteConfig.default()
    if args is not None:
        site_conf.update(args)
    # crawler setting
    settings = {
        **get_project_settings(),
        "DOWNLOAD_DELAY": site_conf["delay"],
        "USER_AGENT": site_conf["ua"],
    }

    current_time = int(time.time())

    if site_id is None:  # update all
        runner.crawl(Crawler(UpdateDcardPostsSpider, settings))
        for site in queries.get_sites_to_update(current_time=current_time):
            run(runner, site["site_id"], args)

    else:
        site = queries.get_site_by_id(site_id=site_id)
        url = site["url"]
        site_conf.update(json.loads(site["config"]))

        if "dcard" in url:
            crawler = Crawler(UpdateDcardPostsSpider, settings)
            crawler.stats.set_value("site_id", site_id)
            runner.crawl(crawler, site_id=site_id)
        else:
            crawler = Crawler(UpdateContentsSpider, settings)
            crawler.stats.set_value("site_id", site_id)
            runner.crawl(
                crawler,
                articles_to_update=get_articles_to_update(site_id, current_time),
                site_id=site_id,
                selenium=site_conf["selenium"],
            )

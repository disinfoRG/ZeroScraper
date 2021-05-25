import time
import os
import pugsql
import json
import logging
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from newsSpiders.types import SiteConfig
from newsSpiders.spiders.basic_update_spider import BasicUpdateSpider
from newsSpiders.spiders.dcard_update_spider import DcardUpdateSpider

logger = logging.getLogger(__name__)
queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))


def get_last_comment_floor(post):
    try:
        last_snapshot_raw_data = queries.get_article_latest_snapshot(
            article_id=post["article_id"]
        )["raw_data"]
    except TypeError:
        return 0

    last_snapshot_comments = json.loads(last_snapshot_raw_data)["comments"]
    if len(last_snapshot_comments) == 0:
        return 0
    elif "floor" not in last_snapshot_comments[-1]:
        return 0
    else:
        return last_snapshot_comments[-1]["floor"]


def get_posts_to_update(posts):
    return [
        {**post, "last_comment_floor": get_last_comment_floor(post)} for post in posts
    ]


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

    site = queries.get_site_by_id(site_id=site_id)
    site_conf.update(json.loads(site["config"]))

    if "dcard" in site["url"]:
        crawler = Crawler(DcardUpdateSpider, settings)
        crawler.stats.set_value("site_id", site_id)
        runner.crawl(
            crawler,
            site_id=site_id,
            posts_to_update=get_posts_to_update(
                queries.get_one_dcard_site_posts_to_update(
                    site_id=site_id, current_time=current_time
                ),
            ),
        )

    else:
        crawler = Crawler(BasicUpdateSpider, settings)
        crawler.stats.set_value("site_id", site_id)
        runner.crawl(
            crawler,
            articles_to_update=queries.get_articles_to_update(
                site_id=site_id, current_time=current_time
            ),
            site_id=site_id,
            site_url=site["url"],
            selenium=site_conf["selenium"],
        )
    logger.debug("finish set up crawl")

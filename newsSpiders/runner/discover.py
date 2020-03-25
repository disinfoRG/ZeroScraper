import json
import pugsql
import os
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from newsSpiders.types import SiteConfig
from newsSpiders.spiders.basic_discover_spider import BasicDiscoverSpider
from newsSpiders.spiders.dcard_dicsover_spider import DcardDiscoverSpider
from newsSpiders.spiders.login_discover_spider import LoginDiscoverSpider


def run(runner, site_id, args=None):
    queries = pugsql.module("./queries")
    queries.connect(os.getenv("DB_URL"))

    site_info = queries.get_site_by_id(site_id=site_id)
    dedup_limit = args["dedup_limit"] or 500
    recent_articles = queries.get_recent_articles_by_site(
        site_id=site_id, limit=dedup_limit
    )

    queries.disconnect()

    site_url = args["url"] or site_info["url"]
    site_type = site_info["type"]
    site_conf = SiteConfig.default()
    site_conf.update(json.loads(site_info["config"]))

    if args is not None:
        site_conf.update(args)

    settings = {
        **get_project_settings(),
        "DEPTH_LIMIT": site_conf["depth"],
        "DOWNLOAD_DELAY": site_conf["delay"],
        "USER_AGENT": site_conf["ua"],
    }

    if "dcard" in site_url:
        crawler = Crawler(DcardDiscoverSpider, settings)
        crawler.stats.set_value("site_id", site_id)

        runner.crawl(
            crawler,
            site_id=site_id,
            site_url=site_url,
            site_type=site_type,
            article_url_excludes=[a["url"] for a in recent_articles],
        )
    elif "appledaily" in site_url:
        crawler = Crawler(LoginDiscoverSpider, settings)
        crawler.stats.set_value("site_id", site_id)

        runner.crawl(
            crawler,
            site_id=site_id,
            site_url=site_url,
            site_type=site_type,
            article_url_patterns=site_conf["article"],
            following_url_patterns=site_conf["following"],
            article_url_excludes=[a["url"] for a in recent_articles],
            selenium=site_conf.get("selenium", False),
            login_url="https://auth.appledaily.com/web/v7/apps/598aee773b729200504d1f31/login",
            credential_tag="appledaily"
        )
    else:
        crawler = Crawler(BasicDiscoverSpider, settings)
        crawler.stats.set_value("site_id", site_id)
        runner.crawl(
            crawler,
            site_id=site_id,
            site_url=site_url,
            site_type=site_type,
            article_url_patterns=site_conf["article"],
            following_url_patterns=site_conf["following"],
            article_url_excludes=[a["url"] for a in recent_articles],
            selenium=site_conf.get("selenium", False),
        )

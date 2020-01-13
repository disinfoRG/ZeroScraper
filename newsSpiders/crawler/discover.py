import json
import zlib
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from newsSpiders.types import SiteConfig
from newsSpiders.spiders.discover_article_spider import DiscoverNewArticlesSpider


def create(runner, queries, site_id, args=None):
    site = queries.get_site_by_id(site_id=site_id)
    site_url = site["url"]
    site_type = site["type"]
    site_conf = SiteConfig.default()
    site_conf.update(json.loads(site["config"]))
    if args is not None:
        site_conf.update(args)

    settings = {
        **get_project_settings(),
        "DEPTH_LIMIT": site_conf["depth"],
        "DOWNLOAD_DELAY": site_conf["delay"],
        "USER_AGENT": site_conf["ua"],
    }

    def links_filter(links):
        return [
            l
            for l in links
            if queries.get_article_by_url(
                url=l.url, url_hash=zlib.crc32(l.url.encode())
            )
            is None
        ]

    runner.crawl(
        Crawler(DiscoverNewArticlesSpider, settings),
        site_id=site_id,
        site_url=site_url,
        site_type=site_type,
        links_filter=links_filter,
        article_url_patterns=site_conf["article"],
        following_url_patterns=site_conf["following"],
        selenium="True" if site_conf["selenium"] else "False",
    )

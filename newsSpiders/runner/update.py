from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from newsSpiders.types import SiteConfig
from newsSpiders.spiders.update_contents_spider import UpdateContentsSpider
from newsSpiders.spiders.update_dcard_spider import UpdateDcardPostsSpider


def run(runner, args=None):
    site_conf = SiteConfig.default()
    if args is not None:
        site_conf.update(args)

    settings = {
        **get_project_settings(),
        "DOWNLOAD_DELAY": site_conf["delay"],
        "USER_AGENT": site_conf["ua"],
    }

    runner.crawl(Crawler(UpdateContentsSpider, settings))
    runner.crawl(Crawler(UpdateDcardPostsSpider, settings))

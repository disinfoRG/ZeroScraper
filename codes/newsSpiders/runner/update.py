import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newsSpiders.types import SiteConfig


def run(args=None):
    site_conf = SiteConfig.default()
    if args is not None:
        site_conf.update(args)
    os.system(
        f"scrapy crawl update_contents \
                -s DOWNLOAD_DELAY={site_conf['delay']} \
                -s USER_AGENT='{site_conf['ua']}'"
    )
    conf = {
        **get_project_settings,
        "DOWNLOAD_DELAY": site_conf["delay"],
        "USER_AGENT": site_conf["ua"],
    }

    process = CrawlerProcess(conf)
    process.crawl("update_contents")
    process.start()

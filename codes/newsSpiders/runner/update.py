import os
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

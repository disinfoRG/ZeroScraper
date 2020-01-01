import os
from newsSpiders.types import SiteConfig


def run(args, default_conf):
    site_conf = default_conf.copy()
    site_conf.update(args)
    os.system(
        f"scrapy crawl update_contents \
                -s DOWNLOAD_DELAY={site_conf['delay']} \
                -s USER_AGENT='{site_conf['ua']}'"
    )

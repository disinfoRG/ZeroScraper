import sqlalchemy as db
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from newsSpiders.types import SiteConfig
from newsSpiders.helpers import connect_to_db
from newsSpiders.spiders.update_contents_spider import UpdateContentsSpider
from newsSpiders.spiders.update_dcard_spider import UpdateDcardPostsSpider


def run(runner, site_id, args=None):
    site_conf = SiteConfig.default()
    if args is not None:
        site_conf.update(args)
    settings = {
        **get_project_settings(),
        "DOWNLOAD_DELAY": site_conf["delay"],
        "USER_AGENT": site_conf["ua"],
    }

    if site_id is None:  # update all
        runner.crawl(Crawler(UpdateContentsSpider, settings))
        runner.crawl(Crawler(UpdateDcardPostsSpider, settings))

    else:
        _, connection, tables = connect_to_db()
        site = tables["Site"]
        query = db.select([site.c.url, site.c.config]).where(site.c.site_id == site_id)
        site_info = dict(connection.execute(query).fetchone())
        url = site_info["url"]
        use_selenium = "True" if "selenium" in site_info["config"].keys() else "False"
        connection.close()

        if "dcard" in url:
            crawler = Crawler(UpdateDcardPostsSpider, settings)
            crawler.stats.set_value("site_id", site_id)
            runner.crawl(crawler, site_id=site_id)
        else:
            crawler = Crawler(UpdateContentsSpider, settings)
            crawler.stats.set_value("site_id", site_id)
            runner.crawl(crawler, site_id=site_id, selenium=use_selenium)

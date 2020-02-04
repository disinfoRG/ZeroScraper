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
    url = None

    if site_id is not None:
        _, connection, tables = connect_to_db()
        site = tables["Site"]

        query = db.select([site.c.url]).where(site.c.site_id == site_id)
        url = connection.execute(query).fetchone()[0]
        connection.close()

    if url is None:
        runner.crawl(Crawler(UpdateContentsSpider, settings))
        runner.crawl(Crawler(UpdateDcardPostsSpider, settings))
    elif "dcard" in url:
        runner.crawl(Crawler(UpdateDcardPostsSpider, settings), site_id=site_id)
    else:
        runner.crawl(Crawler(UpdateContentsSpider, settings), site_id=site_id)

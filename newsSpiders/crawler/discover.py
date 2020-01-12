import sqlalchemy as db
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newsSpiders.helpers import connect_to_db
from newsSpiders.types import SiteConfig


def create(runner, site_id, args=None):
    _, connection, tables = connect_to_db()
    site = tables["Site"]

    query = db.select([site.columns.url, site.columns.type, site.columns.config]).where(
        site.columns.site_id == site_id
    )
    site_info = dict(connection.execute(query).fetchone())
    connection.close()
    site_url = site_info["url"]
    site_type = site_info["type"]
    site_conf = SiteConfig.default()
    site_conf.update(site_info["config"])
    if args is not None:
        site_conf.update(args)

    conf = {
        **get_project_settings(),
        "DEPTH_LIMIT": site_conf["depth"],
        "DOWNLOAD_DELAY": site_conf["delay"],
        "USER_AGENT": site_conf["ua"],
    }

    runner.crawl(
        "discover_new_articles",
        site_id=site_id,
        site_url=site_url,
        site_type=site_type,
        article_url_patterns=site_conf["article"],
        following_url_patterns=site_conf["following"],
        selenium="True" if site_conf["selenium"] else "False",
    )

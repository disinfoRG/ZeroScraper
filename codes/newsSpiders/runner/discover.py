import os
import sqlalchemy as db
from helpers import connect_to_db
from newsSpiders.types import SiteConfig


def run(site_id, args, default_conf):
    _, connection, tables = connect_to_db()
    site = tables["Site"]

    query = db.select([site.columns.url, site.columns.type, site.columns.config]).where(
        site.columns.site_id == site_id
    )
    site_info = dict(connection.execute(query).fetchone())
    site_url = site_info["url"]
    site_type = site_info["type"]
    site_conf = default_conf.copy()
    site_conf.update(site_info["config"])
    site_conf.update(args)

    os.system(
        f"scrapy crawl discover_new_articles \
                -a site_id='{site_id}' \
                -a site_url='{site_url}' \
                -a site_type='{site_type}' \
                -a article_url_patterns='{site_conf['article']}' \
                -a following_url_patterns='{site_conf['following']}' \
                -a selenium='{site_conf['selenium']}' \
                -s DEPTH_LIMIT={site_conf['depth']} \
                -s DOWNLOAD_DELAY={site_conf['delay']} \
                -s USER_AGENT='{site_conf['ua']}'"
    )

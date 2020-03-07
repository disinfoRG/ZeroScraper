import os
import logging
import pugsql
from scrapy.exceptions import DropItem
import time

logger = logging.getLogger(__name__)


class DuplicatesPipeline:
    def __init__(self):
        self.queries = pugsql.module("queries/")

    def open_spider(self, spider):
        self.queries.connect(os.getenv("DB_URL"))

    def process_item(self, item, spider):
        if "article_id" not in item["article"]:
            if (
                self.queries.get_article_id_by_url(
                    url=item["article"]["url"],
                    url_hash=str(item["article"]["url_hash"]),
                )
                is not None
            ):
                # XXX for shorter log messages
                del item["article_snapshot"]
                raise DropItem(f"Duplicate item: {item['article']['url']}")
            else:
                return item
        else:
            return item


class InvalidItemsError(Exception):
    pass


class MySqlPipeline(object):
    def __init__(self):
        self.queries = pugsql.module("queries")

    def open_spider(self, spider):
        self.queries.connect(os.getenv("DB_URL"))

    def process_article(self, item):
        if "article_id" not in item:
            article_id = self.queries.insert_article(**item)
            logger.debug(f"inserted new article {article_id}")
            self.queries.update_site_crawl_time(
                site_id=item["site_id"], last_crawl_at=int(time.time())
            )
            return article_id

        else:
            r = self.queries.update_article_snapshot_time(
                article_id=item["article_id"],
                last_snapshot_at=item["last_snapshot_at"],
                snapshot_count=item["snapshot_count"],
                next_snapshot_at=item["next_snapshot_at"],
            )
            logger.debug(f'updated {r} article {item["article_id"]}')
            return item["article_id"]

    def process_item(self, item, spider):
        article = item["article"]
        snapshot = item["article_snapshot"]

        with self.queries.transaction() as t:
            article_id = self.process_article(article)
            if snapshot is not None:
                snapshot.setdefault("article_id", article_id)
                if snapshot["article_id"] != article_id:
                    raise InvalidItemsError("Article id mismatch with snapshot")
                self.queries.insert_snapshot(**snapshot)

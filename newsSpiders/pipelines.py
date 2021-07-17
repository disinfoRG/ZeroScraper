import zlib
import os
import logging
import pugsql
from datetime import timedelta
from scrapy.exceptions import DropItem
import time
from newsSpiders.kombuqueue import connection, queue_snapshot
from newsSpiders.types import NewSnapshotMessage, ProcessEvent, asdict

logger = logging.getLogger(__name__)


class StandardizePipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if "update" in spider.name:
            return item

        url = item["article"]["url"]
        domains = ["udn", "chinatimes", "appledaily", "thenewslens", "storm.mg"]

        if any(d in url for d in domains):
            url = url.split("?")[0]
            url_hash = zlib.crc32(url.encode())
            item["article"]["url"] = url
            item["article"]["url_hash"] = url_hash

        return item


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


class OldArticlesPipeline:
    """
    A pipeline that detects if the article is over 2 months old since it's first discovered.
    If so, do not insert new snapshot and update next_snapshot_at to 0
    """

    def __init__(self):
        self.queries = pugsql.module("queries/")

    def open_spider(self, spider):
        self.queries.connect(os.getenv("DB_URL"))

    def process_item(self, item, spider):
        if "article_id" in item["article"]:
            article_info = self.queries.get_article_by_id(
                article_id=item["article"]["article_id"]
            )
            first_snapshot_at = article_info["first_snapshot_at"]
            keep_alive_duration = int(timedelta(days=60).total_seconds())
            if (
                first_snapshot_at
                <= item["article"]["last_snapshot_at"] - keep_alive_duration
            ):
                del item["article_snapshot"]
                self.queries.close_snapshot(article_id=item["article"]["article_id"])
                raise DropItem(f"Item too old: {item['article']['article_id']}")
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
            article.setdefault("article_id", article_id)
            if snapshot is not None:
                snapshot.setdefault("article_id", article_id)
                if snapshot["article_id"] != article_id:
                    raise InvalidItemsError("Article id mismatch with snapshot")
                self.queries.insert_snapshot(**snapshot)
        return item


class KombuPipeline:
    def process_item(self, item, spider):
        article = item["article"]
        snapshot = item["article_snapshot"]
        with connection() as conn:
            queue_snapshot(conn, article, snapshot)
            logger.debug(
                f"putting {article['article_id']} {snapshot['snapshot_at']} in kombu"
            )
        return item

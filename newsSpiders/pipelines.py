import os
import pugsql
from scrapy.exceptions import DropItem
import time


class DuplicatesPipeline:
    def __init__(self):
        self.queries = pugsql.module("queries")

    def open_spider(self, spider):
        self.queries.connect(os.getenv("DB_URL"))

    def process_item(self, item, spider):
        if spider.name in ("discover_new_articles", "dcard_discover"):
            if (
                self.queries.get_article_id_by_url(
                    url=item["article"]["url"], url_hash=item["article"]["url_hash"]
                )
                is not None
            ):
                # XXX for shorter log messages
                item["article_snapshot"]["raw_data"] = "<removed>"
                raise DropItem(f"Duplicate item: {item['article']['url']}")
            else:
                return item
        else:
            return item


class MySqlPipeline(object):
    def __init__(self):
        self.queries = pugsql.module("queries")

    def open_spider(self, spider):
        self.queries.connect(os.getenv("DB_URL"))

    def close_spider(self, spider):
        self.queries.disconnect()

    def process_item(self, item, spider):
        article = item["article"]
        snapshot = item["article_snapshot"]

        if spider.name in ("discover_new_articles", "dcard_discover"):
            article_id = self.queries.insert_article(**article)
            print(f"article {article_id} inserted!")
            snapshot["article_id"] = article_id
            self.queries.insert_snapshot(
                article_id=snapshot["article_id"],
                crawl_time=snapshot["snapshot_at"],
                raw_data=snapshot["raw_data"],
            )
            self.queries.update_site_crawl_time(
                site_id=article["site_id"], crawl_time=int(time.time())
            )

        elif spider.name in ("update_contents", "dcard_update"):
            # update Article
            self.queries.update_article_snapshot_time(
                article_id=article["article_id"],
                crawl_time=article["last_snapshot_at"],
                snapshot_count=article["snapshot_count"],
                next_snapshot_at=article["next_snapshot_at"],
            )

            # insert to ArticleSnapshot
            self.queries.insert_snapshot(
                article_id=snapshot["article_id"],
                crawl_time=snapshot["snapshot_at"],
                raw_data=snapshot["raw_data"],
            )

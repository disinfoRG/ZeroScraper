# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pugsql
import os

queries = pugsql.module("queries/")


class DuplicateURLPipeline:
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        url = item["url"]
        if url in self.urls_seen:
            raise DropItem("Duplicate url found: %s" % url)
        else:
            self.urls_seen.add(url)
            return item


class SQLWritePipeline:
    def open_spider(self, spider):
        queries.connect(os.getenv("DB_URL", default="sqlite:///db.sqlite3"))

    def process_item(self, item, spider):
        with queries.transaction():
            r = queries.find_first_article({"url": item["url"]})
            if r is not None:
                article_id = r["article_id"]
            else:
                article = {"url": item["url"]}
                article_id = queries.update_article(article)
            queries.update_article_snapshot(
                {"article_id": article_id, "raw_body": item["body"]}
            )
        return item

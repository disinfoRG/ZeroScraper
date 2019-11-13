# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pugsql

queries = pugsql.module("queries/")


class SQLWritePipeline:
    def open_spider(self, spider):
        queries.connect("sqlite:///db.sqlite3")

    def process_item(self, item, spider):
        with queries.transaction():
            article = {"url": item["url"]}
            article_id = queries.update_article(article)
            queries.update_article_snapshot(
                {"article_id": article_id, "raw_body": item["body"],}
            )
        return item

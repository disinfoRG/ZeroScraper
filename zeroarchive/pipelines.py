# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pugsql

queries = pugsql.module("queries/")

class MySQLWritePipeline:
    def open_spider(self, spider):
        queries.connect("sqlite:///db.sqlite")

    def process_item(self, item, spider):
        queries.update_article(item)
        return item

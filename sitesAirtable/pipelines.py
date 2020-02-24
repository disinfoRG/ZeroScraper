# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pugsql
import os
import json
from scrapy.exceptions import DropItem
from sitesAirtable.items import site_type_mapping

queries = pugsql.module("queries/")


def upsert_site(queries, value):
    site = queries.get_site_by_airtable_id(airtable_id=value["airtable_id"])
    if site is not None:
        queries.update_site(site_id=site["site_id"], **value)
    else:
        queries.insert_site(value)


class SiteItemPipeline(object):
    def process_item(self, item, spider):
        if item["type"] not in site_type_mapping.keys():
            raise DropItem(f"Unknown site type '{item['type']}'")
        else:
            item["type"] = site_type_mapping[item["type"]]
        return item


class MySQLPipeline(object):
    def open_spider(self, spider):
        queries.connect(os.getenv("DB_URL"))

    def process_item(self, item, spider):
        upsert_site(
            queries,
            {
                "airtable_id": item["airtable_id"],
                "is_active": item["is_active"],
                "name": item["name"],
                "type": item["type"],
                "url": item["url"],
                "config": json.dumps(item["config"]),
                "site_info": json.dumps(item["site_info"]),
            },
        )

        return item

    def close_spider(self, spider):
        queries.disconnect()


print(queries)

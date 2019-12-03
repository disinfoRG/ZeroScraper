# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pugsql
import os
import json

queries = pugsql.module("queries/")

site_type_mapping = {
    "官媒": "official_media",
    "內容農場": "content_farm",
    "組織官網": "organization_website",
    "Fb 專頁": "fb_page",
    "Fb 公開社團": "fb_public_group",
    "Ptt 看板": "ptt_board",
    "YouTube 頻道": "youtube_channel",
    "YouTube 帳號": "youtube_user",
}

config_fields = ["article", "following", "depth", "delay", "ua"]


class MySQLPipeline(object):
    def open_spider(self, spider):
        queries.connect(os.getenv("DB_URL"))

    def process_item(self, item, spider):
        if item["type"] not in site_type_mapping.keys():
            return item
        item["type"] = site_type_mapping[item["type"]]
        item["config"] = json.dumps({k: item[k] for k in config_fields if k in item})

        queries.upsert_site(
            {
                "airtable_id": item["id"],
                "name": item["name"],
                "type": item["type"],
                "url": item["url"],
                "config": item["config"],
            }
        )

        return item

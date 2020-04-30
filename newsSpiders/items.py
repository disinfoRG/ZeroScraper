# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    article_id = scrapy.Field()
    site_id = scrapy.Field()
    url = scrapy.Field()
    url_hash = scrapy.Field()
    article_type = scrapy.Field()
    first_snapshot_at = scrapy.Field()
    last_snapshot_at = scrapy.Field()
    next_snapshot_at = scrapy.Field()
    snapshot_count = scrapy.Field()
    redirect_to = scrapy.Field()


class ArticleSnapshotItem(scrapy.Item):
    article_id = scrapy.Field()
    snapshot_at = scrapy.Field()
    raw_data = scrapy.Field()

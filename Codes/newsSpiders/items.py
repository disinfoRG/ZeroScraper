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
    url_hash_seq = scrapy.Field()
    found_at = scrapy.Field()
    fetched_at = scrapy.Field()
    last_fetched_at = fetched_at
    next_fetch_at = scrapy.Field()
    fetch_count = scrapy.Field()
    redirect_from = scrapy.Field()
    raw_body = scrapy.Field()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

site_type_mapping = {
    "官媒": "official_media",
    "新聞網站": "news_website",
    "內容農場": "content_farm",
    "組織官網": "organization_website",
    "Fb 專頁": "fb_page",
    "Fb 公開社團": "fb_public_group",
    "討論區看板": "discussion_board",
    "YouTube 頻道": "youtube_channel",
    "YouTube 帳號": "youtube_user",
}

site_config_fields = ["article", "following", "login_url", "depth", "delay", "ua", "selenium"]


class SiteItem(scrapy.Item):
    airtable_id = scrapy.Field()
    approved = scrapy.Field()
    is_active = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    config = scrapy.Field()
    site_info = scrapy.Field()

import scrapy
import re
import json
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
import sqlalchemy as db
from newsSpiders.helpers import generate_next_fetch_time, connect_to_db
import time


class DcardSpider(scrapy.Spider):
    name = "dcard"

    def __init__(
        self,
        site_id="",
        site_url="https://www.dcard.tw/f/trending?latest=true",
        site_type="",
        *args,
        **kwargs,
    ):
        super(DcardSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.site_type = site_type
        self.site_url = site_url
        self.selenium = False
        self.forum_name = re.search("/f/(.*)", self.site_url).group(1).split("?")[0]

    def start_requests(self):
        # todo: the limit
        api_url = f"https://www.dcard.tw/_api/forums/{self.forum_name}/posts?popular=false&limit=100"

        yield scrapy.Request(url=api_url, callback=self.get_post_id)

    def get_post_id(self, response):
        response_json = json.loads(response.body)
        post_ids = [str(x["id"]) for x in response_json]

        # todo: filter??
        post_urls = [
            f"https://www.dcard.tw/f/{self.forum_name}/p/{pid}" for pid in post_ids
        ]

        comment_api = [
            f"https://www.dcard.tw/_api/posts/{pid}/comments" for pid in post_ids
        ]

    def get_comments(self, response):

        raise

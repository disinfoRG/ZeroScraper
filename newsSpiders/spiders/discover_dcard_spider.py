import scrapy
import re
import json
import zlib
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_fetch_time
import time


class DiscoverDcardPostsSpider(scrapy.Spider):
    name = "dcard_discover"

    def __init__(
        self, site_id="", site_url="", site_type="", *args, **kwargs,
    ):
        super(DiscoverDcardPostsSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.site_type = site_type
        self.site_url = site_url
        self.selenium = False
        self.forum_name = re.search("/f/(.*)", self.site_url).group(1).split("?")[0]

    def start_requests(self):
        api_url = f"https://www.dcard.tw/_api/forums/{self.forum_name}/posts?popular=false&limit=100"

        yield scrapy.Request(url=api_url, callback=self.get_post_id)

    def get_post_id(self, response):
        response_json = json.loads(response.body.decode("utf-8"))
        post_ids = [str(x["id"]) for x in response_json]

        for i in range(len(post_ids)):
            pid = post_ids[i]
            post_api = f"https://www.dcard.tw/_api/posts/{pid}"

            yield scrapy.Request(
                url=post_api, callback=self.get_posts, cb_kwargs={"post_id": pid},
            )

    def get_posts(self, response, post_id):
        response_json = json.loads(response.body.decode("utf-8"))
        comment_api = f"https://www.dcard.tw/_api/posts/{post_id}/comments?limit=100"
        yield scrapy.Request(
            url=comment_api,
            callback=self.get_comments,
            cb_kwargs={"post_id": post_id, "post_info": response_json},
        )

    def get_comments(self, response, post_id, post_info):
        comments_api_result = json.loads(response.body.decode("utf-8"))
        # prepare Items
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        # get current time
        parse_time = int(time.time())

        # populate article item
        article["site_id"] = self.site_id
        article["url"] = f"https://www.dcard.tw/f/{self.forum_name}/p/{post_id}"
        article["url_hash"] = zlib.crc32(article["url"].encode())
        article["article_type"] = "Dcard"
        article["first_snapshot_at"] = parse_time
        article["last_snapshot_at"] = parse_time
        article["snapshot_count"] = 1
        article["next_snapshot_at"] = generate_next_fetch_time(
            self.site_type, article["snapshot_count"], parse_time
        )

        # populate article_snapshot item
        post_comments = {"post": post_info, "comments": comments_api_result}
        article_snapshot["raw_data"] = json.dumps(post_comments)
        article_snapshot["snapshot_at"] = parse_time

        yield {"article": article, "article_snapshot": article_snapshot}

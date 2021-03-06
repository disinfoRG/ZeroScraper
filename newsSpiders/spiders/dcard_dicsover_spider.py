import scrapy
import re
import json
import zlib
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_snapshot_time
import time


post_id_pattern = re.compile("https://www.dcard.tw/f/[^/]*/p/(\d+)")


def parse_post_id(link):
    m = post_id_pattern.match(link)
    return m.group(1)


class DcardDiscoverSpider(scrapy.Spider):
    name = "dcard_discover"

    def __init__(
        self, site_id="", site_url="", article_url_excludes=None, *args, **kwargs
    ):
        super(DcardDiscoverSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.site_url = site_url
        self.selenium = False
        self.forum_name = re.search("/f/(.*)", self.site_url).group(1).split("?")[0]
        if article_url_excludes is None:
            self.post_id_excludes = []
        else:
            self.post_id_excludes = [parse_post_id(url) for url in article_url_excludes]

    def start_requests(self):
        api_url = f"https://www.dcard.tw/_api/forums/{self.forum_name}/posts?popular=false&limit=100"

        yield scrapy.Request(url=api_url, callback=self.get_post_id)

    def get_post_id(self, response):
        response_json = json.loads(response.body.decode("utf-8"))
        post_ids = [str(x["id"]) for x in response_json]

        for pid in post_ids:
            if pid in self.post_id_excludes:
                self.logger.debug(f"Found duplicated post {pid}")
                continue

            post_api = f"https://www.dcard.tw/_api/posts/{pid}"

            yield scrapy.Request(
                url=post_api, callback=self.get_posts, cb_kwargs={"post_id": pid}
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
        now = int(time.time())

        # populate article item
        article["site_id"] = self.site_id
        article["url"] = f"https://www.dcard.tw/f/{self.forum_name}/p/{post_id}"
        article["url_hash"] = zlib.crc32(article["url"].encode())
        article["article_type"] = "Dcard"
        article["first_snapshot_at"] = now
        article["last_snapshot_at"] = now
        article["snapshot_count"] = 1
        article["next_snapshot_at"] = generate_next_snapshot_time(
            "dcard", article["snapshot_count"], now
        )
        article["redirect_to"] = None

        # populate article_snapshot item
        post_comments = {"post": post_info, "comments": comments_api_result}
        article_snapshot["raw_data"] = json.dumps(post_comments)
        article_snapshot["snapshot_at"] = now

        yield {"article": article, "article_snapshot": article_snapshot}

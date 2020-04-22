import scrapy
import re
import json
import zlib
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_snapshot_time
import time


article_id_pattern = re.compile("https://www.toutiao.com/a(\d+)/")


def parse_article_id(link):
    m = article_id_pattern.match(link)
    if m:
        return m.group(1)


class ToutiaoDiscoverSpider(scrapy.Spider):
    name = "toutiao_discover"

    def __init__(
        self,
        site_id="",
        site_url="",
        site_type="",
        article_url_excludes=None,
        *args,
        **kwargs,
    ):
        super(ToutiaoDiscoverSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.site_type = site_type
        self.site_url = site_url
        self.selenium = False
        if article_url_excludes is None:
            self.article_id_excludes = []
        else:
            self.article_id_excludes = [
                parse_article_id(url) for url in article_url_excludes
            ]

    def start_requests(self):
        api_url = f"https://www.toutiao.com/api/pc/realtime_news/"

        yield scrapy.Request(url=api_url, callback=self.get_article_urls)

    def get_article_urls(self, response):
        response_json = json.loads(response.body.decode("utf-8"))["data"]
        article_ids = [
            re.search(r"/group/(\d+)/", x["open_url"]).group(1) for x in response_json
        ]

        for aid in article_ids:
            if aid in self.article_id_excludes:
                self.logger.debug(f"Found duplicated post {aid}")
                continue

            article_url = f"https://www.toutiao.com/a{aid}/"

            yield scrapy.Request(url=article_url, callback=self.parse_articles)

    def parse_articles(self, response):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        # get current time
        now = int(time.time())

        # populate article item
        article["site_id"] = self.site_id
        article["url"] = response.url
        article["article_type"] = "Article"
        article["first_snapshot_at"] = now
        article["last_snapshot_at"] = now
        article["snapshot_count"] = 1
        article["next_snapshot_at"] = generate_next_snapshot_time(
            self.site_type, article["snapshot_count"], now
        )
        if "redirect_urls" in response.meta.keys():
            article["url"] = response.request.meta["redirect_urls"][0]
            article["redirect_to"] = response.url
        else:
            article["redirect_to"] = None
        article["url_hash"] = zlib.crc32(article["url"].encode())

        # populate article_snapshot item
        article_snapshot["raw_data"] = response.text
        article_snapshot["snapshot_at"] = now

        yield {"article": article, "article_snapshot": article_snapshot}

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ast import literal_eval
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_fetch_time
import zlib
import time


class DiscoverNewArticlesSpider(CrawlSpider):
    name = "discover_new_articles"

    def __init__(
        self,
        site_id="",
        site_url="",
        site_type="",
        article_url_patterns="",
        following_url_patterns="",
        selenium="",
        *args,
        **kwargs
    ):
        super(DiscoverNewArticlesSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.site_url = site_url
        self.start_urls = [site_url]
        self.site_type = site_type
        self.selenium = literal_eval(selenium)
        article_url_patterns = article_url_patterns.split("; ")
        following_url_patterns = following_url_patterns.split("; ")
        social_media_links = [
            "facebook.com",
            "twitter.com",
            "linkedin.com",
            "plurk.com" "line.me",
            "line.naver.jp",
            "plus.google.com",
        ]
        DiscoverNewArticlesSpider.rules = [
            Rule(
                LinkExtractor(allow=article_url_patterns, deny=social_media_links),
                callback="parse_articles",
            )
        ]
        if following_url_patterns:
            DiscoverNewArticlesSpider.rules.append(
                Rule(LinkExtractor(allow=following_url_patterns), follow=True)
            )
        super(DiscoverNewArticlesSpider, self)._compile_rules()

    def assign_article_type(self):
        if "ptt.cc" in self.site_url:
            article_type = "PTT"
        elif "dcard" in self.site_url:
            article_type = "Dcard"
        else:
            article_type = "Article"
        return article_type

    def parse_articles(self, response):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        # get current time
        parse_time = int(time.time())

        # populate article item
        article["site_id"] = self.site_id
        article["url"] = response.url
        article["url_hash"] = zlib.crc32(article["url"].encode())
        article["article_type"] = self.assign_article_type()
        article["first_snapshot_at"] = parse_time
        article["last_snapshot_at"] = parse_time
        article["snapshot_count"] = 1
        article["next_snapshot_at"] = generate_next_fetch_time(
            self.site_type, article["snapshot_count"], parse_time
        )
        if "redirect_urls" in response.meta.keys():
            article["url"] = response.request.meta["redirect_urls"][0]
            article["redirect_to"] = response.url

        # populate article_snapshot item
        article_snapshot["raw_data"] = response.text
        article_snapshot["snapshot_at"] = parse_time

        yield {"article": article, "article_snapshot": article_snapshot}

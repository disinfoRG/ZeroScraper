from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_snapshot_time
import zlib
import time


class BasicDiscoverSpider(CrawlSpider):
    name = "basic_discover"

    def __init__(
        self,
        site_id="",
        site_url="",
        article_url_patterns="",
        following_url_patterns="",
        article_url_excludes=None,
        selenium=False,
        *args,
        **kwargs,
    ):
        super(BasicDiscoverSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.site_url = site_url
        self.start_urls = [site_url]
        self.selenium = selenium
        self.article_url_excludes = (
            article_url_excludes if article_url_excludes is not None else []
        )
        article_url_patterns = article_url_patterns.split("; ")
        following_url_patterns = following_url_patterns.split("; ")
        social_media_links = [
            "facebook.com",
            "twitter.com",
            "linkedin.com",
            "plurk.com",
            "line.me",
            "line.naver.jp",
            "plus.google.com",
        ]
        BasicDiscoverSpider.rules = [
            Rule(
                LinkExtractor(allow=article_url_patterns, deny=social_media_links),
                process_links=self.dedup_article_links,
                callback="parse_articles",
            )
        ]
        if following_url_patterns:
            BasicDiscoverSpider.rules.append(
                Rule(LinkExtractor(allow=following_url_patterns), follow=True)
            )
        super(BasicDiscoverSpider, self)._compile_rules()
        if site_id:
            self.name = f"{self.name}:{site_id}"

    def is_duplicate_url(self, link):
        if link.url in self.article_url_excludes:
            self.logger.debug(f"Found duplicated article url {link.url}")
            return True
        else:
            return False

    def dedup_article_links(self, article_links):
        if len(self.article_url_excludes) == 0:
            return article_links
        return [link for link in article_links if not self.is_duplicate_url(link)]

    def assign_article_type(self):
        if "ptt.cc" in self.site_url:
            article_type = "PTT"
        else:
            article_type = "Article"
        return article_type

    def parse_articles(self, response):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        # get current time
        now = int(time.time())

        # populate article item
        article["site_id"] = self.site_id
        article["url"] = response.url
        article["article_type"] = self.assign_article_type()
        article["first_snapshot_at"] = now
        article["last_snapshot_at"] = now
        article["snapshot_count"] = 1
        article["next_snapshot_at"] = generate_next_snapshot_time(
            self.site_url, article["snapshot_count"], now
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

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_fetch_time
import zlib
import time


class DiscoverSplashSpider(CrawlSpider):
    name = "discover_splash"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810},
        'SPIDER_MIDDLEWARES': {'scrapy_splash.SplashDeduplicateArgsMiddleware': 100},
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
}

    def __init__(
        self,
        site_id="",
        site_url="",
        site_type="",
        article_url_patterns="",
        following_url_patterns="",
        article_url_excludes=None,
        selenium=False,
        *args,
        **kwargs,
    ):
        super(DiscoverSplashSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.site_url = site_url
        self.site_type = site_type
        self.selenium = selenium
        self.article_url_excludes = (
            article_url_excludes if article_url_excludes is not None else []
        )
        self.article_url_patterns = article_url_patterns.split("; ")
        self.following_url_patterns = following_url_patterns.split("; ")
        self.social_media_links = [
            "facebook.com",
            "twitter.com",
            "linkedin.com",
            "plurk.com",
            "line.me",
            "line.naver.jp",
            "plus.google.com",
        ]

        if site_id:
            self.name = f"{self.name}:{site_id}"

    def start_requests(self):
        yield SplashRequest(self.site_url)
        rules = (
            Rule(
                LinkExtractor(allow=self.article_url_patterns, deny=self.social_media_links),
                process_links=self.dedup_article_links,
                process_request=self.splash_request_article,
                callback="parse_articles",
            ),
            Rule(LinkExtractor(allow=self.following_url_patterns),
                 process_request=self.splash_request_follow,
                 follow=True)
            )

    def splash_request_article(self, request):
        return SplashRequest(url=request.url, meta={'real_url': request.url}, callback="parse_articles")

    def splash_request_follow(self, request):
        return SplashRequest(url=request.url, meta={'real_url': request.url})


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
        parse_time = int(time.time())

        # populate article item
        article["site_id"] = self.site_id
        article["url"] = response.meta['real_url']
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
        else:
            article["redirect_to"] = None

        # populate article_snapshot item
        article_snapshot["raw_data"] = response.text
        article_snapshot["snapshot_at"] = parse_time

        yield {"article": article, "article_snapshot": article_snapshot}

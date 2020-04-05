from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_splash import SplashRequest
from newsSpiders.spiders.basic_discover_spider import BasicDiscoverSpider


class SplashDiscoverSpider(BasicDiscoverSpider):
    name = "splash_discover"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810},
        'SPIDER_MIDDLEWARES': {'scrapy_splash.SplashDeduplicateArgsMiddleware': 100},
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
}

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def start_requests(self):
        yield SplashRequest(self.site_url)
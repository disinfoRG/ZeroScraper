from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime, timedelta


class NewsSpider(CrawlSpider):
    name = 'news'

    def __init__(self, site_id='', site_url='', article_url_patterns='', following_url_patterns='', *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.start_urls = [site_url]
        article_url_patterns = article_url_patterns.split('; ')
        following_url_patterns = following_url_patterns.split('; ')
        print(article_url_patterns)
        NewsSpider.rules = [Rule(LinkExtractor(allow=article_url_patterns), callback="parse_articles")]
        if following_url_patterns:
            NewsSpider.rules.append(Rule(LinkExtractor(allow=following_url_patterns), follow=True))
        super(NewsSpider, self)._compile_rules()

    def parse_articles(self, response):
        parse_time = datetime.utcnow() + timedelta(hours=8)
        parse_time = str(parse_time.strftime('%Y-%m-%d-%H:%M:%S'))
        yield {"from_site": self.site_id,
               "url": response.url,
               "title": " ".join(response.css('h1 *::text').extract()).strip(),
               "raw_body": response.text,
               "fetched_at": parse_time}


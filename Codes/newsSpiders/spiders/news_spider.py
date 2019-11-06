from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime, timedelta
from newsSpiders.items import ArticleItem


class NewsSpider(CrawlSpider):
    name = 'news'

    def __init__(self, site_id='', site_url='', article_url_patterns='', following_url_patterns='', *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.start_urls = [site_url]
        article_url_patterns = article_url_patterns.split('; ')
        following_url_patterns = following_url_patterns.split('; ')
        NewsSpider.rules = [Rule(LinkExtractor(allow=article_url_patterns), callback="parse_articles")]
        if following_url_patterns:
            NewsSpider.rules.append(Rule(LinkExtractor(allow=following_url_patterns), follow=True))
        super(NewsSpider, self)._compile_rules()

    def parse_articles(self, response):
        article = ArticleItem()
        parse_time = datetime.utcnow() + timedelta(hours=8)
        parse_time = str(parse_time.strftime('%Y-%m-%d-%H:%M:%S'))
        article['site_id'] = self.site_id
        article['url'] = response.url
        article['raw_body'] = response.text
        article['found_at'] = parse_time
        article['fetched_at'] = parse_time
        article['article_id'] = article['url'] + '/' + article['found_at']
        if 'redirect_urls' in response.meta.keys():
            article['redirect_from'] = response.meta['redirect_urls']

        yield article

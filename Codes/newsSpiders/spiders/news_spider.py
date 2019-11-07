from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime, timedelta
from newsSpiders.items import ArticleItem


class NewsSpider(CrawlSpider):
    name = 'news'

    def __init__(self, site_id='', site_url='', site_type = '', article_url_patterns='', following_url_patterns='', *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.start_urls = [site_url]
        self.site_type = site_type
        article_url_patterns = article_url_patterns.split('; ')
        following_url_patterns = following_url_patterns.split('; ')
        NewsSpider.rules = [Rule(LinkExtractor(allow=article_url_patterns), callback="parse_articles")]
        if following_url_patterns:
            NewsSpider.rules.append(Rule(LinkExtractor(allow=following_url_patterns), follow=True))
        super(NewsSpider, self)._compile_rules()

    def parse_articles(self, response):
        article = ArticleItem()
        parse_time = datetime.utcnow() + timedelta(hours=8)
        parse_time_str = parse_time.strftime('%Y-%m-%d-%H:%M:%S')
        article['site_id'] = self.site_id
        article['url'] = response.url
        article['raw_body'] = response.text
        article['found_at'] = parse_time_str
        article['fetched_at'] = parse_time_str
        article['last_fetched_at'] = parse_time_str
        #todo: modify next_fetched time based on site_type
        article['next_fetch_at'] = (parse_time + timedelta(days=1)).strftime('%Y-%m-%d-%H:%M:%S')
        article['fetch_count'] = 1
        article['article_id'] = article['url'] + '/' + article['found_at']
        if 'redirect_urls' in response.meta.keys():
            article['redirect_from'] = response.meta['redirect_urls']

        yield article

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime, timedelta
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
import jsonlines
import os
import sys
sys.path.append('../')
from helpers import generate_next_fetch_time


class DiscoverNewArticlesSpider(CrawlSpider):
    name = 'discover_new_articles'

    def __init__(self, site_id='', site_url='', site_type='', article_url_patterns='', following_url_patterns='', *args, **kwargs):
        super(DiscoverNewArticlesSpider, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.start_urls = [site_url]
        self.site_type = site_type
        data_dir = os.getcwd().split('/NewsScraping/')[0] + '/NewsScraping/Data'
        try:
            self.existing_urls = [obj['redirect_from'][0] if obj['redirect_from'] else obj['url']
                                  for obj in jsonlines.open(f'{data_dir}/article.jsonl') if obj['site_id'] == self.site_id]

        except FileNotFoundError:
            self.existing_urls = list()
        article_url_patterns = article_url_patterns.split('; ')
        following_url_patterns = following_url_patterns.split('; ')
        DiscoverNewArticlesSpider.rules = [Rule(LinkExtractor(allow=article_url_patterns,
                                                              deny=self.existing_urls), callback="parse_articles")]
        if following_url_patterns:
            DiscoverNewArticlesSpider.rules.append(Rule(LinkExtractor(allow=following_url_patterns), follow=True))
        super(DiscoverNewArticlesSpider, self)._compile_rules()

    def parse_articles(self, response):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        # get current time
        parse_time = datetime.utcnow() + timedelta(hours=8)
        parse_time_str = parse_time.strftime('%Y-%m-%d-%H:%M:%S')

        # populate article item
        article['site_id'] = self.site_id
        article['url'] = response.url
        article['found_at'] = parse_time_str
        article['last_fetched_at'] = parse_time_str
        article['fetch_count'] = 1
        article['next_fetch_at'] = generate_next_fetch_time(self.site_type, article['fetch_count'], parse_time)
        article['article_id'] = article['url'] + '/' + article['found_at']
        article['redirect_from'] = response.meta['redirect_urls'] if 'redirect_urls' in response.meta.keys() else None

        # populate article_snapshot item
        article_snapshot['raw_body'] = response.text
        article_snapshot['fetched_at'] = parse_time_str
        article_snapshot['article_id'] = article['article_id']

        yield {'article': article, 'article_snapshot': article_snapshot}

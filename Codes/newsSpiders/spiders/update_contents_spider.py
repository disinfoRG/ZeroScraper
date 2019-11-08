import scrapy
from ast import literal_eval
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from datetime import datetime, timedelta


# still working...
# todo: a wrapper for this spider

class UpdateContentsSpider(scrapy.Spider):
    name = "update_contents"

    def __init__(self, article_urls=[], *args, **kwargs):
        super(UpdateContentsSpider, self).__init__(*args, **kwargs)
        self.start_urls = literal_eval(article_urls)

    def parse(self, response):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        parse_time = datetime.utcnow() + timedelta(hours=8)
        parse_time_str = parse_time.strftime('%Y-%m-%d-%H:%M:%S')

        # populate article item
        article['last_fetched_at'] = parse_time_str
        article['redirect_from'] = response.meta['redirect_urls'] if 'redirect_urls' in response.meta.keys() else None

        # populate article_snapshot item
        article_snapshot['raw_body'] = response.text
        article_snapshot['fetched_at'] = parse_time_str
        article_snapshot['article_id'] = article['article_id']

        yield {'article': article, 'article_snapshot': article_snapshot}

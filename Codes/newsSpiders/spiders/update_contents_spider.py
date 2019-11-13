import scrapy
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from datetime import datetime, timedelta
import jsonlines
import os
from dateutil.parser import parse
import json
import sys
sys.path.append('../')
from helpers import generate_next_fetch_time


# still working...
class UpdateContentsSpider(scrapy.Spider):
    name = "update_contents"

    def __init__(self, *args, **kwargs):
        super(UpdateContentsSpider, self).__init__(*args, **kwargs)
        root_dir = os.getcwd().split('/NewsScraping/')[0] + '/NewsScraping'
        data_dir = root_dir + '/Data'
        current_taiwan_time = datetime.utcnow() + timedelta(hours=8)
        self.articles_to_update = [obj for obj in jsonlines.open(f'{data_dir}/article.jsonl')
                                   if obj['next_fetch_at'] and parse(obj['next_fetch_at']) < current_taiwan_time]
        self.url_map = json.load(open(f'{data_dir}/url_map.json', 'r'))

    def start_requests(self):
        for a in self.articles_to_update:
            yield scrapy.Request(url=a['url'], callback=self.update_article,
                                 cb_kwargs={k: a[k] for k in ['site_id', 'article_id', 'url', 'found_at', 'fetch_count']})

    def update_article(self, response, site_id, article_id, url, found_at, fetch_count):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        parse_time = datetime.utcnow() + timedelta(hours=8)
        parse_time_str = parse_time.strftime('%Y-%m-%d-%H:%M:%S')
        site_type = self.url_map[site_id]['type']

        # populate article item
        # copy from the original article
        article['site_id'] = site_id
        article['article_id'] = article_id
        article['url'] = url
        article['found_at'] = found_at
        # update
        article['last_fetched_at'] = parse_time_str
        article['redirect_from'] = response.meta['redirect_urls'] if 'redirect_urls' in response.meta.keys() else None
        article['fetch_count'] = fetch_count + 1
        article['next_fetch_at'] = generate_next_fetch_time(site_type, article['fetch_count'], parse_time)

        # populate article_snapshot item
        article_snapshot['raw_body'] = response.text
        article_snapshot['fetched_at'] = parse_time_str
        article_snapshot['article_id'] = article['article_id']

        yield {'article': article, 'article_snapshot': article_snapshot}

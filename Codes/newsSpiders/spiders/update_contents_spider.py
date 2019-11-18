import scrapy
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from datetime import datetime, timedelta
import sqlalchemy as db
import os
import json
import sys
sys.path.append('../')
from helpers import generate_next_fetch_time, connect_to_db
import time


class UpdateContentsSpider(scrapy.Spider):
    name = "update_contents"

    def __init__(self, *args, **kwargs):
        super(UpdateContentsSpider, self).__init__(*args, **kwargs)
        root_dir = os.getcwd().split('/NewsScraping/')[0] + '/NewsScraping'
        data_dir = root_dir + '/Data'
        current_time = datetime.utcnow() + timedelta(hours=8)  # taiwan time
        int_current_time = int(current_time.strftime('%y%m%d%H%M'))
        engine, connection = connect_to_db()
        article = db.Table('Article', db.MetaData(), autoload=True, autoload_with=engine)
        query = db.select([article.columns.url, article.columns.url_hash, article.columns.site_id, article.snapshot_count])
        query = query.where(db.and_(article.columns.next_snapshot_at != 0, article.columns.next_snapshot_at < int_current_time))
        self.articles_to_update = [dict(row) for row in connection.execute(query)]
        self.url_map = json.load(open(f'{data_dir}/url_map.json', 'r'))

    def start_requests(self):
        for a in self.articles_to_update:
            yield scrapy.Request(url=a['url'], callback=self.update_article,
                                 cb_kwargs={'url_hash': a['url_hash'], 'site_id': a['site_id'], 'snapshot_count': a['snapshot_count']})

    def update_article(self, response, url_hash, site_id, snapshot_count):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        parse_time = int(time.time())
        site_type = self.url_map[site_id]['type']

        # populate article item
        # copy from the original article
        article['url_hash'] = url_hash
        # update
        article['last_snapshot_at'] = parse_time
        article['snapshot_count'] = snapshot_count+1
        article['next_snapshot_at'] = generate_next_fetch_time(site_type, article['snapshot_count'], parse_time)

        # populate article_snapshot item
        article_snapshot['raw_body'] = response.text
        article_snapshot['snapshot_at'] = parse_time
        article_snapshot['article_id'] = article['article_id']

        yield {'article': article, 'article_snapshot': article_snapshot}

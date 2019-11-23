import scrapy
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
import sqlalchemy as db
import sys
sys.path.append('../')
from helpers import generate_next_fetch_time, connect_to_db
import time


class UpdateContentsSpider(scrapy.Spider):
    name = "update_contents"

    def __init__(self, *args, **kwargs):
        super(UpdateContentsSpider, self).__init__(*args, **kwargs)
        int_current_time = int(time.time())
        engine, connection = connect_to_db()
        article = db.Table('Article', db.MetaData(), autoload=True, autoload_with=engine)
        query = db.select([article.c.article_id, article.c.url, article.c.site_id, article.c.snapshot_count])
        query = query.where(db.and_(article.c.next_snapshot_at != 0, article.c.next_snapshot_at < int_current_time))
        self.articles_to_update = [dict(row) for row in connection.execute(query)]
        self.site = db.Table('Site', db.MetaData(), autoload=True, autoload_with=engine)
        self.connection = connection

    def start_requests(self):
        for a in self.articles_to_update:
            yield scrapy.Request(url=a['url'], callback=self.update_article,
                                 cb_kwargs={'article_id': a['article_id'], 'site_id': a['site_id'], 'snapshot_count': a['snapshot_count']})

    def update_article(self, response, article_id, site_id, snapshot_count):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        parse_time = int(time.time())
        query = db.select([self.site.columns.type]).where(self.site.columns.site_id == site_id)
        site_type = self.connection.execute(query).fetchone()[0]

        # populate article item
        # copy from the original article
        article['article_id'] = article_id
        # update
        article['last_snapshot_at'] = parse_time
        article['snapshot_count'] = snapshot_count+1
        article['next_snapshot_at'] = generate_next_fetch_time(site_type, article['snapshot_count'], parse_time)

        # populate article_snapshot item
        article_snapshot['raw_data'] = response.text
        article_snapshot['snapshot_at'] = parse_time
        article_snapshot['article_id'] = article_id

        yield {'article': article, 'article_snapshot': article_snapshot}

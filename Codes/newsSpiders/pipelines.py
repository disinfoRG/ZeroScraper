import os
import sqlalchemy as db
from sqlalchemy.sql.expression import bindparam
import sys
sys.path.append('../')
from helpers import connect_to_db


#TODO:
"""
1. how to retrieve article_id for article snapshot -- can we use url_hash as instead of article_id in article_snapshot??
2. should send to sql one at a time or in batch. If one at a time can retrieve article_id -- maybe change to one at a time in case batch fails
2. increase length for datetime obj? int(11) is only between -2147483648 to 0 to 2147483647
3. site_id type on mysql (change to varchar) -- what about site table
"""

#TODO:
"""
1. turn datetime to unix timestamp -- get to only seconds
# import time; int(time.time()) 
2. change to article_id instead of url_hash for update_article
3. os.env https://www.geeksforgeeks.org/python-os-getenv-method/
"""


class MySqlPipeline(object):

    def __init__(self):
        self.data_dir = os.getcwd().split('/NewsScraping/')[0] + '/NewsScraping/Data'
        self.connection = None
        self.db_tables = None
        self.values_list = None

    def open_spider(self, spider):
        engine, connection = connect_to_db()
        self.connection = connection
        metadata = db.MetaData()
        self.db_tables = {'article': db.Table('Article', metadata, autoload=True, autoload_with=engine),
                          'article_snapshot': db.Table('ArticleSnapshot', metadata, autoload=True, autoload_with=engine)}
        self.values_list = {'article': [],
                            'article_snapshot': []}

    def close_spider(self, spider):
        if spider.name == 'update_contents':
            # update Article
            article_table = self.db_tables['article']
            # todo: finish change join key to article_id
            query = article_table.update().where(article_table.c.article_id == bindparam('id'))
            query = query.values({'snapshot_count': bindparam('snapshot_count'),
                                  'last_snapshot_at': bindparam('last_snapshot_at'),
                                  'next_snapshot_at': bindparam('next_snapshot_at')})

            self.connection.execute(query, self.values_list['article'])

            # insert to ArticleSnapshot
            query = db.insert(self.db_tables['article_snapshot'])
            self.connection.execute(query, self.values_list['article_snapshot'])
        self.connection.close()

    def process_item(self, item, spider):
        if spider.name == 'discover_new_articles':
            query = db.insert(self.db_tables['article'])
            exe = self.connection.execute(query, item['article'])
            article_id = exe.inserted_primary_key
            item['article_snapshot']['article_id'] = article_id
            query = db.insert(self.db_tables['article_snapshot'])
            self.connection.execute(query, item['article_snapshot'])

        # todo: change to insert one-by-one later
        elif spider.name == 'update_contents':
            for key in item.keys():
                query = db.insert(self.db_tables[key])
                self.connection.execute(query, item[key])
                self.values_list[key].append(item[key])




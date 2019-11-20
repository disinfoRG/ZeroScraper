import os
import sqlalchemy as db
from sqlalchemy.sql.expression import bindparam
import sys
sys.path.append('../')
from helpers import connect_to_db

#TODO:
"""
0. os.env https://www.geeksforgeeks.org/python-os-getenv-method/
"""


class MySqlPipeline(object):

    def __init__(self):
        root_dir = os.getcwd().split('NewsScraping')[0] + 'NewsScraping'
        self.data_dir = root_dir+'/Data'
        self.connection = None
        self.db_tables = None
        self.values_list = None
        self.update_article_query = None

    def open_spider(self, spider):
        engine, connection = connect_to_db()
        self.connection = connection
        metadata = db.MetaData()
        self.db_tables = {'article': db.Table('Article', metadata, autoload=True, autoload_with=engine),
                          'article_snapshot': db.Table('ArticleSnapshot', metadata, autoload=True, autoload_with=engine)}
        self.update_article_query = self.db_tables['article'].update().where(self.db_tables['article'].c.article_id == bindparam('id'))
        self.update_article_query = self.update_article_query.values({'snapshot_count': bindparam('snapshot_count'),
                                                                      'last_snapshot_at': bindparam('last_snapshot_at'),
                                                                      'next_snapshot_at': bindparam('next_snapshot_at')})

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if spider.name == 'discover_new_articles':
            query = db.insert(self.db_tables['article'])
            exe = self.connection.execute(query, item['article'])
            article_id = exe.inserted_primary_key
            item['article_snapshot']['article_id'] = article_id
            query = db.insert(self.db_tables['article_snapshot'])
            self.connection.execute(query, item['article_snapshot'])

        elif spider.name == 'update_contents':
            # update Article
            article_dict = dict(item['article'])
            article_dict['id'] = article_dict.pop('article_id')  # because cannot use article_id in bindparam
            self.connection.execute(self.update_article_query, article_dict)

            # insert to ArticleSnapshot
            query = db.insert(self.db_tables['article_snapshot'])
            self.connection.execute(query, item['article_snapshot'])




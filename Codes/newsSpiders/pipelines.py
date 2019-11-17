import os
import sqlalchemy as db
sys.path.append('../')
from helpers import connect_to_db

"""
1. how to retrieve article_id for article snapshot
2. increase length for datetime obj?
3. site_id type on mysql
4. revise time comparison in update_content 
"""


class MultiJSONPipeline(object):

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
        if spider.name == 'discover_new_articles':
            print(self.values_list['article'])
            for key in self.values_list:
                query = db.insert(key)
                self.connection.execute(query, self.values_list[key])

    def process_item(self, item, spider):
        if spider.name == 'discover_new_articles':
            for key in item.keys():
                self.values_list[key].append(item[key])

        elif spider.name == 'update_contents':
            print(item['article'])



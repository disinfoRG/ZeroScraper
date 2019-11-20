import os
package_path = os.getcwd().split('NewsScraping')[0]+'NewsScraping'
import sys
sys.path.append(f'{package_path}/Codes')
import sqlalchemy as db
import json
from helpers import connect_to_db

SITE_NAME = '每日頭條'
SITE_URL = 'https://kknews.cc/'
SITE_TYPE = 'content-farm'
ARTICLE_MAP = "/([a-zA-Z]+)/([0-9a-zA-Z]+).html"
FOLLOWING_MAP = "/([a-z]+)/$"
engine, connection = connect_to_db()
site = db.Table('Site', db.MetaData(), autoload=True, autoload_with=engine)
site_info = {'name': SITE_NAME, 'url': SITE_URL, 'type': SITE_TYPE, 'config': {"article": ARTICLE_MAP, "following": FOLLOWING_MAP}}
site_info['config'] = json.dumps(site_info['config'])

connection.execute(db.insert(site), site_info)

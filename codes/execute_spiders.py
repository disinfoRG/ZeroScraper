import argparse
import os
from datetime import datetime, timedelta
from dateutil.parser import parse
import sqlalchemy as db
from ast import literal_eval
from helpers import connect_to_db

parser = argparse.ArgumentParser()
parser.add_argument('--site_id', help="site id to crawl")
parser.add_argument('--depth', default=3, help='desired depth limit; 0 if no limit imposed.', type=int)
parser.add_argument('--delay', default=1.5, help='time delayed for request.')
parser.add_argument('--google_bot', action='store_true', help='if mask crawler as googlebot')
parser.add_argument('-d', '--discover', action='store_true', help='execute spider to discover new articles')
parser.add_argument('-u', '--update', action='store_true', help='execute spider to update articles')

# set up
args = parser.parse_args()
root_dir = os.getcwd().split('/NewsScraping/')[0]+'/NewsScraping'
if args.google_bot:
    user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
else:
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
engine, connection = connect_to_db()
site = db.Table('Site', db.MetaData(), autoload=True, autoload_with=engine)


# execute
os.system(f"cd {root_dir}/Codes/newsSpiders")
if args.discover:
    args.site_id = int(args.site_id)
    query = db.select([site.columns.url, site.columns.type, site.columns.config]).where(
        site.columns.site_id == args.site_id)
    site_info = dict(connection.execute(query).fetchone())
    site_info['config'] = literal_eval(site_info['config'])
    site_url = site_info['url']
    site_type = site_info['type']
    article_pattern = site_info['config']['article']
    following_pattern = site_info['config'].get('following', "")

    os.system(f"scrapy crawl discover_new_articles \
                -a site_id='{args.site_id}' \
                -a site_url='{site_url}' \
                -a site_type='{site_type}' \
                -a article_url_patterns='{article_pattern}' \
                -a following_url_patterns='{following_pattern}' \
                -s DEPTH_LIMIT={args.depth} \
                -s DOWNLOAD_DELAY={args.delay} \
                -s USER_AGENT='{user_agent}'")

elif args.update:
    os.system(f"scrapy crawl update_contents \
                -s DOWNLOAD_DELAY={args.delay} \
                -s USER_AGENT='{user_agent}'")
else:
    raise Exception('Please specify action by adding either --discover or --update flag')

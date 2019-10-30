import argparse
import os
import pickle as pk

parser = argparse.ArgumentParser()
parser.add_argument('--site_id', help="site id to crawl")
parser.add_argument('--depth', default=3, help='desired depth limit; 0 if no limit imposed.', type=int)
parser.add_argument('--delay', default=1.5, help='time delayed for request.')
parser.add_argument('--google_bot', action='store_true', help='if mask crawler as googlebot')

args = parser.parse_args()
url_map = pk.load(open('url_map.pk', 'rb'))
site_url = url_map[args.site_id]['url']
article_map = url_map[args.site_id]['article']

if args.google_bot:
    user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
else:
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    user_agent = 'newsSpider'

try:
    following_map = url_map[args.site_id]['following']
except KeyError:
    following_map = ''

os.system(f"scrapy crawl news \
            -a site_url='{site_url}'\
            -a article_url_patterns='{article_map}' \
            -a following_url_patterns='{following_map}' \
            -s DEPTH_LIMIT={args.depth} \
            -s DOWNLOAD_DELAY={args.delay} \
            -s USER_AGENT='{user_agent}' \
            -o {args.site_id}.csv")


"""
access each line in Data/article.jsonl, if next_fetched_at time is smaller than now, go to the url again to collect raw body
next, modify next_fetch_at and fetch_count
"""

import os
import jsonlines
from datetime import datetime, timedelta
from dateutil.parser import parse
import requests


def is_earlier_than_now(given_datetime):
    if isinstance(given_datetime, str):
        given_datetime = parse(given_datetime)
    elif isinstance(given_datetime, datetime):
        pass
    else:
        raise Exception('given_datetime has to be either type string or type datetime')
    current_taiwan_time = datetime.utcnow()+timedelta(hours=8)
    return given_datetime < current_taiwan_time


data_dir = os.getcwd().split('/NewsScraping/')[0] + '/NewsScraping/Data'
articles = (obj for obj in jsonlines.open('Data/article.jsonl'))

with jsonlines.open(f'{data_dir}/article_temp_output.jl', mode='w') as temp_writer, \
        jsonlines.open(f'{data_dir}/article_snapshot.jsonl', mode='w') as snapshot_writer:
    for obj in articles:
        if obj['next_fetch_at'] and is_earlier_than_now(obj['next_fetch_at']):
            snapshot_obj = dict()
            crawl_time = (datetime.utcnow()+timedelta(hours=8)).strftime('%Y-%m-%d-%H:%M:%S')
            r = requests.get(obj['url'], headers={'User-Agent': 'Chrome/76.0.3809.132 Safari/537.36'})
            snapshot_obj['article_id'] = obj['article_id']
            snapshot_obj['raw_body'] = r.text
            snapshot_obj['fetched_at'] = crawl_time
            snapshot_writer.write(snapshot_obj)

            updated_article_obj = obj.copy()
            updated_article_obj['fetch_count'] += 1
            updated_article_obj['last_fetched_at'] = crawl_time
            if updated_article_obj['fetch_count'] < 7:
                updated_article_obj['next_fetch_at'] = (parse(crawl_time) + timedelta(days=1)).strftime('%Y-%m-%d-%H:%M:%S')
            elif 7 <= updated_article_obj['fetch_count'] < 11:
                updated_article_obj['next_fetch_at'] = (parse(crawl_time) + timedelta(weeks=1)).strftime('%Y-%m-%d-%H:%M:%S')
            else:
                updated_article_obj['next_fetch_at'] = None
            temp_writer.write(updated_article_obj)

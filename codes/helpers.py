from datetime import datetime, timedelta
import json
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()


def connect_to_db():
    engine = create_engine(os.getenv("DB_URL"))
    connection = engine.connect()

    return engine, connection


def generate_next_fetch_time(site_type, fetch_count, parse_time):
    """
    A method that generates next fetch time based on site type
    :param site_type: str, the type of site where articles are from
    :param fetch_count: int, how many times have this article fetched?
    :param parse_time: a unix timestamp
    :return: next fetch time, in unix timestamp
    """
    # turn to datetime object
    parse_time = datetime.fromtimestamp(parse_time)
    # Default
    if 7 > fetch_count >= 1:
        next_fetch_time = parse_time + timedelta(days=1)
        return datetime.timestamp(next_fetch_time)
    else:
        return 0

    # if site_type == 'content_farm':
    #     # 1/day for 1 week, 1/week for 1 month
    #     if 11 > fetch_count >= 7:
    #         next_fetch_time = (parse_time + timedelta(weeks=1)).strftime('%y%m%d%H%M')
    #         return int(next_fetch_time)
    #     elif 7 > fetch_count >= 1:
    #         next_fetch_time = (parse_time + timedelta(days=1)).strftime('%y%m%d%H%M%S')
    #         return int(next_fetch_time)
    #     else:
    #         return 0
    #
    # elif site_type == 'news_website':
    #     # 1/hour for 1 day
    #     if fetch_count < 24:
    #         next_fetch_time = (parse_time + timedelta(hours=1)).strftime('%y%m%d%H%M')
    #         return next_fetch_time
    #     else:
    #         return 0
    # elif site_type == 'organization_website':
    #     if 7 > fetch_count >= 1:
    #         next_fetch_time = (parse_time + timedelta(days=1)).strftime('%y%m%d%H%M')
    #         return next_fetch_time

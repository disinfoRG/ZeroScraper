import argparse
import os
from itertools import groupby

import pugsql
import pytz
from dateutil.parser import parse
from datetime import datetime, timedelta

queries = pugsql.module('queries')
queries.connect(os.getenv("DB_URL"))


def date_to_unix(dt, timezone='Asia/Taipei'):
    tw = pytz.timezone(timezone)
    loc_dt = tw.localize(dt)
    start_unix = loc_dt.timestamp()
    end_unix = start_unix + 86400 - 1
    return start_unix, end_unix


def prep_entry_for_insert(stats_list):
    for k, v in groupby(sorted(stats_list, key=lambda x: x['site_id']), key=lambda x: x['site_id']):
        dicts = list(v)
        result = {'discover_count': 0, 'update_count': 0}
        for d in dicts: result.update(d)
        yield result


def main(args):
    # parse date string to datetime obj
    dt = parse(args.date)
    # uniformly format date, for use in db insertion
    datestr = dt.strftime('%Y-%m-%d')

    date_unix = date_to_unix(dt)
    discover_stats = list(queries.count_articles_discovered_in_interval(time_start=date_unix[0], time_end=date_unix[1]))
    update_stats = list(queries.count_articles_updated_in_interval(time_start=date_unix[0], time_end=date_unix[1]))
    combined_stats_list = discover_stats + update_stats
    for entry in prep_entry_for_insert(combined_stats_list):
        queries.upsert_stats({**entry, 'date': datestr})


if __name__ == '__main__':
    utc_now = datetime.utcnow()
    tw_now = utc_now + timedelta(hours=8)
    tw_yesterday = tw_now.date()-timedelta(days=1)
    str_tw_yesterday = tw_yesterday.strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date to calculate stats on", type=str, default=str_tw_yesterday)

    args = parser.parse_args()
    main(args)

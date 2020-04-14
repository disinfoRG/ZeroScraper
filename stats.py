import argparse
import os
import pugsql
from dateutil.parser import parse
from datetime import datetime, timedelta
import pytz


def date_to_unix(date_str, timezone='Asia/Taipei'):
    date = parse(date_str)
    tw = pytz.timezone(timezone)
    loc_dt = tw.localize(date)
    start_unix = loc_dt.timestamp()
    end_unix = start_unix + 86400
    return start_unix, end_unix


def main(args):
    queries = pugsql.module('queries')
    queries.connect(os.getenv("DB_URL"))

    date_start_unix, date_end_unix = date_to_unix(args.date)

    for stats in queries.count_site_stats(time_start=date_start_unix,
                                          time_end=date_end_unix):
        queries.upsert_stats({**stats, 'date': args.date})


if __name__ == '__main__':
    utc_now = datetime.utcnow()
    tw_now = utc_now + timedelta(hours=8)
    tw_yesterday = tw_now.date()-timedelta(days=1)
    str_tw_yesterday = tw_yesterday.strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date to calculate stats on", type=str, default=str_tw_yesterday)

    args = parser.parse_args()
    main(args)

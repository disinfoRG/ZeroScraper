#!/usr/bin/env python

from newsSpiders.itertools import grouper
from pathlib import Path
import argparse
import datetime
import json
import logging
import newsSpiders.pugsql as pugsql
import os
import re
import sys
import traceback

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)
queries = pugsql.module("queries")

table_pat = re.compile("^(article)?snapshot\d*$", re.I)
duration_pat = re.compile("^(\d+)([wd])")


def parse_args():
    def to_day_start(date):
        return datetime.datetime.fromisoformat(str(date))

    def to_day_end(date):
        return to_day_start(date + datetime.timedelta(days=1))

    def date_range(value):
        start, end = value.split(":", 1)
        end_date = to_day_end(datetime.date.fromisoformat(end))
        start_date = None
        m = duration_pat.match(start)
        if m:
            if m.group(2) == "w":
                start_date = end_date - datetime.timedelta(weeks=int(m.group(1)))
            elif m.group(2) == "d":
                start_date = end_date - datetime.timedelta(days=int(m.group(1)))
            else:
                raise ValueError(f"invalid duration {start}")
        else:
            start_date = to_day_start(datetime.date.fromisoformat(start))
        logger.debug(f"select snapshot from {start_date} to {end_date}")
        return {
            "start_date": int(start_date.timestamp()),
            "end_date": int(end_date.timestamp()),
        }

    def table(value):
        if not table_pat.match(value):
            raise ValueError(f"invalid table name {value}")
        return value

    parser = argparse.ArgumentParser(
        description="dump article snapshot table data into JSONLines format"
    )
    parser.add_argument(
        "-t",
        "--table",
        type=table,
        help="name of the snapshot table to dump",
        required=True,
    )
    parser.add_argument(
        "-o", "--output", help="output filename; to STDOUT if not provided"
    )
    parser.add_argument(
        "-r",
        "--date-range",
        type=date_range,
        help="select only snapshots taken in given date range specified in '<start_date>:<end_date>' or '<duration>:<end_date>'; date format must be 'YYYY-MM-DD'; duration may be '<n>d', '<n>w'.",
    )
    args = parser.parse_args()
    return args


def dump_snapshots(queries, fh, date_range=None):
    i = 0
    for batch in grouper(queries.get_snapshot_ats(date_range=date_range), 1000):
        snapshot_ats = [row["snapshot_at"] for row in batch if row]
        for snapshot in queries.get_snapshots_by_snapshot_at(snapshot_ats=snapshot_ats):
            fh.write(
                json.dumps(
                    {
                        key: snapshot[key]
                        for key in ["article_id", "snapshot_at", "raw_data"]
                        if key in snapshot
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            i += 1
        logger.info(f"dumped snapshot #{i}")
    logger.info(f"dumped total {i} snapshots")


def load_dynamic_queries(queries, table):
    """
    Load queries to a pugsql module base on `table` value.  Many hacks.
    """
    # check SQL injection
    if not table_pat.match(table):
        raise ValueError(f"invalid table name {table}")
    queries.add_query(
        f"""-- :name get_snapshot_ats_all :many
        SELECT DISTINCT(snapshot_at) FROM {table}
        """
    )
    queries.add_query(
        f"""-- :name get_snapshot_ats_date_ranged :many
        SELECT DISTINCT(snapshot_at) FROM {table}
        WHERE snapshot_at BETWEEN :start_date AND (:end_date - 1)
        """
    )
    queries.add_query(
        f"""-- :name get_snapshots_by_snapshot_at :many
        SELECT article_id, snapshot_at, raw_data FROM {table}
        WHERE snapshot_at in :snapshot_ats
        """
    )

    def get_snapshot_ats(queries, date_range=None):
        if date_range is None:
            return queries.get_snapshot_ats_all()
        else:
            return queries.get_snapshot_ats_date_ranged(**date_range)

    queries.add_method("get_snapshot_ats", get_snapshot_ats)


def main(table, output=None, date_range=None):
    load_dynamic_queries(queries, table)
    queries.connect(os.getenv("DB_URL"))
    try:
        if output is None:
            dump_snapshots(queries, sys.stdout, date_range=date_range)
        else:
            with Path(output).open("w") as fh:
                dump_snapshots(queries, fh, date_range=date_range)
    except Exception:
        logger.error(traceback.format_exc())
    queries.disconnect()


if __name__ == "__main__":
    sys.exit(main(**vars(parse_args())))

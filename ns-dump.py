#!/usr/bin/env python

import logging
import traceback
import argparse
import os
import sys
import json
import datetime
from pathlib import Path
import re
import pugsql
import pugsql.parser

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
        help="name of the snapshot table to archive",
        required=True,
    )
    parser.add_argument(
        "-o", "--output", help="output filename; to STDOUT if not provide"
    )
    parser.add_argument(
        "-r",
        "--date-range",
        type=date_range,
        help="select only snapshots taken in given date range specified in '<start_date>:<end_date>' or '<duration>:<end_date>'; date format must be 'YYYY-MM-DD'; duration may be '<n>d', '<n>w'.",
    )
    args = parser.parse_args()
    return args


def add_query(queries, stmt):
    """
    Dynamically add queries to pugsql modules.  A hack.
    """
    s = pugsql.parser.parse(stmt, ctx=None)
    if hasattr(queries, s.name):
        raise ValueError('Please choose another name than "%s".' % s.name)
    s.set_module(queries)
    setattr(queries, s.name, s)
    queries._statements[s.name] = s


def get_snapshots_in_keys(queries, date_range=None):
    if date_range is None:
        return queries.get_snapshots_in_keys()
    else:
        return queries.get_snapshots_in_date_range_in_keys(**date_range)


def dump_snapshots(queries, fh, date_range=None):
    i = 0
    for key in get_snapshots_in_keys(queries, date_range=date_range):
        snapshot = queries.get_snapshot_by_keys(**key)
        fh.write(
            json.dumps(
                {
                    key: value
                    for key, value in snapshot.items()
                    if key in ["article_id", "snapshot_at", "raw_data"]
                },
                ensure_ascii=False,
            )
            + "\n"
        )
        if i % 10000 == 0:
            logger.info(f"exported snapshot #{i}")
        i += 1
    logger.info(f"exported total {i} snapshots")


def load_dynamic_queries(queries, table):
    add_query(
        queries,
        f"""-- :name get_snapshots_in_keys :many
        SELECT article_id, snapshot_at FROM {table}
        """,
    )
    add_query(
        queries,
        f"""-- :name get_snapshots_in_date_range_in_keys :many
        SELECT article_id, snapshot_at FROM {table}
        WHERE snapshot_at >= :start_date AND snapshot_at < :end_date
        """,
    )
    add_query(
        queries,
        f"""-- :name get_snapshot_by_keys :one
        SELECT article_id, snapshot_at, raw_data FROM {table}
        WHERE article_id = :article_id AND snapshot_at = :snapshot_at
        """,
    )


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
    import sys

    sys.exit(main(**vars(parse_args())))

#!/usr/bin/env python

import os
import sys
from pathlib import Path
import argparse
import re
import json
import logging
import traceback
import newsSpiders.pugsql as pugsql
from newsSpiders.itertools import grouper

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)
queries = pugsql.module("queries")

table_pat = re.compile("^(article)?snapshot\d*$", re.I)


def parse_args():
    def table(value):
        if not table_pat.match(value):
            raise ValueError(f"invalid table name {value}")
        return value

    parser = argparse.ArgumentParser(
        description="load article snapshot table data from JSONLines format"
    )
    parser.add_argument(
        "-t",
        "--table",
        type=table,
        help="name of the snapshot table to load",
        required=True,
    )

    parser.add_argument(
        "-i", "--input", help="input filename; from STDIN if not provided"
    )
    args = parser.parse_args()
    return args


def load_dynamic_queries(queries, table):
    queries.add_query(
        f"""-- :name replace_snapshots :insert
        REPLACE {table} (article_id, snapshot_at, raw_data, snapshot_at_date)
        VALUES (:article_id, :snapshot_at, :raw_data, FROM_UNIXTIME(:snapshot_at))
        """
    )


def load_snapshots(queries, fh):
    i = 0
    for lines in grouper(fh, 1000):
        snapshots = [
            {
                key: value
                for key, value in json.loads(line.rstrip()).items()
                if key in ["article_id", "snapshot_at", "raw_data"]
            }
            for line in lines
            if line
        ]
        queries.replace_snapshots(*snapshots)
        if i % 10000 == 0:
            logger.info(f"loaded snapshot #{i}")
        i += len(snapshots)
    logger.info(f"loaded total {i} snapshots")


def main(table, input=None):
    load_dynamic_queries(queries, table)
    queries.connect(os.getenv("DB_URL"))
    try:
        if input is None:
            load_snapshots(queries, sys.stdin)
        else:
            with Path(input).open("r") as fh:
                load_snapshots(queries, fh)
    except Exception:
        logger.error(traceback.format_exc())
    queries.disconnect()


if __name__ == "__main__":
    import sys

    sys.exit(main(**vars(parse_args())))

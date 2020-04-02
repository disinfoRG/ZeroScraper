#!/usr/bin/env python

import logging
import argparse
import os
import json
from pathlib import Path
import pugsql
import pugsql.parser

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)
queries = pugsql.module("queries")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--table", help="name of the snapshot table to archive", required=True
    )
    parser.add_argument("-o", "--output", help="output filename", required=True)
    return parser.parse_args()


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


def main(table, output):
    add_query(
        queries,
        f"""-- :name get_snapshots :many
        SELECT article_id, snapshot_at, raw_data FROM {table}
        LIMIT 10
        """,
    )

    queries.connect(os.getenv("DB_URL"))
    try:
        with Path(output).open("w") as fh:
            i = 0
            for snapshot in queries.get_snapshots():
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
                    logger.info(f"exporting snapshot #{i}")
                i += 1
        logger.info(f"exported {i} snapshots")
    except Exception as e:
        logger.error(e)
    queries.disconnect()


if __name__ == "__main__":
    import sys

    sys.exit(main(**vars(parse_args())))

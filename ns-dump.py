#!/usr/bin/env python

import logging
import traceback
import argparse
import os
import sys
import json
from pathlib import Path
import pugsql
import pugsql.parser

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)
queries = pugsql.module("queries")


def parse_args():
    parser = argparse.ArgumentParser(
        description="dump article snapshot table data into JSONLines format"
    )
    parser.add_argument(
        "-t", "--table", help="name of the snapshot table to archive", required=True
    )
    parser.add_argument(
        "-o", "--output", help="output filename; to STDOUT if not provide"
    )
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


def write_export(fh):
    i = 0
    for key in queries.get_snapshots_in_keys():
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


def main(table, output=None):
    add_query(
        queries,
        f"""-- :name get_snapshots_in_keys :many
        SELECT article_id, snapshot_at FROM {table}
        """,
    )
    add_query(
        queries,
        f"""-- :name get_snapshot_by_keys :one
        SELECT article_id, snapshot_at, raw_data FROM {table}
        WHERE article_id = :article_id AND snapshot_at = :snapshot_at
        """,
    )

    queries.connect(os.getenv("DB_URL"))
    try:
        if output is None:
            write_export(sys.stdout)
        else:
            with Path(output).open("w") as fh:
                write_export(fh)
    except Exception:
        logger.error(traceback.format_exc())
    queries.disconnect()


if __name__ == "__main__":
    import sys

    sys.exit(main(**vars(parse_args())))

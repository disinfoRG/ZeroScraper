#!/usr/bin/env python3

import argparse
import pugsql
import os
import datetime
from tabulate import tabulate

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newsSpiders.runner import discover, update

queries = pugsql.module("./queries")
queries.connect(os.getenv("DB_URL"))


def main(args):

    if args.command == "discover":
        process = CrawlerProcess(get_project_settings())
        discover.run(process, args.id, vars(args))
        process.start()

    elif args.command == "update":
        print("updating articles from site " + str(args.id))
        process = CrawlerProcess(get_project_settings())
        update.run(process, args.id, vars(args))
        process.start()

    elif args.command == "activate":
        print("activate")
        for site_id in args.id:
            queries.activate_site(site_id=site_id)

    elif args.command == "deactivate":
        for site_id in args.id:
            queries.deactivate_site(site_id=site_id)

    elif args.command == "list":
        print(
            tabulate(
                [
                    [
                        site["site_id"],
                        site["name"],
                        site["url"],
                        ("v" if site["is_active"] else ""),
                        (
                            datetime.datetime.fromtimestamp(site["last_crawl_at"])
                            if site["last_crawl_at"]
                            else ""
                        ),
                        site["airtable_id"],
                    ]
                    for site in queries.get_all_sites()
                ],
                headers=["id", "name", "url", "active", "last crawl at", "airtable id"],
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title="sub command", dest="command", required=True)

    discover_cmd = cmds.add_parser("discover", help="do discover")
    discover_cmd.add_argument(
        "id", type=int, help="id of the site to discover in news db", nargs="?"
    )
    discover_cmd.add_argument("--url", type=str, help="start url", nargs="?")
    discover_cmd.add_argument(
        "--article", type=str, help="article url pattern", nargs="?"
    )
    discover_cmd.add_argument(
        "--following", type=str, help="following url pattern", nargs="?"
    )
    discover_cmd.add_argument(
        "--depth", help="desired depth limit; 0 if no limit imposed.", type=int
    )
    discover_cmd.add_argument(
        "--dedup-limit",
        help="number of recent articles url to store in memory",
        type=int,
    )
    discover_cmd.add_argument("--delay", help="time delayed for request.", type=int)
    discover_cmd.add_argument("--ua", help="user_agent", type=str)

    update_cmd = cmds.add_parser("update", help="do update")
    update_cmd.add_argument(
        "id", type=int, help="id of the site to update in news db", nargs="?"
    )
    update_cmd.add_argument("--delay", help="time delayed for request.")
    update_cmd.add_argument("--ua", help="user_agent")

    activate_cmd = cmds.add_parser("activate", help="activate a site in news db")
    activate_cmd.add_argument(
        "id", type=int, help="id of the site to be set to active", nargs="+"
    )

    deactivate_cmd = cmds.add_parser("deactivate", help="deactivate a site in news db")
    deactivate_cmd.add_argument(
        "id", type=int, help="id of the site to be deactivated", nargs="+"
    )

    list_cmd = cmds.add_parser("list", help="list all sites")

    args = parser.parse_args()
    main(args)

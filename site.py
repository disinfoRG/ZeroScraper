import argparse
import pugsql
import os
import time
from dotenv import load_dotenv

load_dotenv()

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newsSpiders.runner import discover, update

queries = pugsql.module("./queries")
queries.connect(os.getenv("DB_URL"))


def main(args):

    if args.command == "discover":
        process = CrawlerProcess(get_project_settings())
        crawl_time = int(time.time())
        queries.update_site_crawl_time(site_id=args.id, crawl_time=crawl_time)
        discover.run(process, args.id, vars(args))
        process.start()

    elif args.command == "update":
        print("updating articles from site " + str(args.id))
        process = CrawlerProcess(get_project_settings())
        update.run(process, args.id, vars(args))
        process.start()

    elif args.command == "activate":
        print("activate")
        queries.activate_site(site_id=args.id)

    elif args.command == "deactivate":
        queries.deactivate_site(site_id=args.id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title="sub command", dest="command", required=True)

    discover_cmd = cmds.add_parser("discover", help="do discover")
    discover_cmd.add_argument(
        "id", type=int, help="id of the site to discover in news db", nargs="?"
    )
    discover_cmd.add_argument(
        "--depth", help="desired depth limit; 0 if no limit imposed.", type=int
    )
    discover_cmd.add_argument("--delay", help="time delayed for request.")
    discover_cmd.add_argument("--ua", help="user_agent")
    discover_cmd.add_argument("--selenium", help="use selenium to load website or not.")

    update_cmd = cmds.add_parser("update", help="do update")
    update_cmd.add_argument(
        "id", type=int, help="id of the site to update in news db", nargs="?"
    )
    update_cmd.add_argument("--delay", help="time delayed for request.")
    update_cmd.add_argument("--ua", help="user_agent")
    update_cmd.add_argument("--selenium", help="use selenium to load website or not.")

    activate_cmd = cmds.add_parser("activate", help="activate a site in news db")
    activate_cmd.add_argument(
        "id", type=int, help="id of the site to be set to active", nargs="?"
    )

    deactivate_cmd = cmds.add_parser("deactivate", help="deactivate a site in news db")
    deactivate_cmd.add_argument(
        "id", type=int, help="id of the site to be deactivated", nargs="?"
    )

    args = parser.parse_args()
    main(args)

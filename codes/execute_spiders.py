import argparse
import os
import sqlalchemy as db
from helpers import connect_to_db
from newsSpiders.runner import discover, update
from newsSpiders.types import SiteConfig


parser = argparse.ArgumentParser()
parser.add_argument("--site_id", type=int, help="site id to crawl")
parser.add_argument(
    "--depth", help="desired depth limit; 0 if no limit imposed.", type=int
)
parser.add_argument("--delay", help="time delayed for request.")
parser.add_argument("--ua", help="user_agent")
parser.add_argument("--selenium", help="use selenium to load website or not.")
parser.add_argument(
    "-d",
    "--discover",
    action="store_true",
    help="execute spider to discover new articles",
)
parser.add_argument(
    "-u", "--update", action="store_true", help="execute spider to update articles"
)

# set up
args = parser.parse_args()

# execute
if args.discover:
    discover.run(args.site_id, vars(args))
elif args.update:
    update.run(vars(args))
else:
    raise Exception(
        "Please specify action by adding either --discover or --update flag"
    )

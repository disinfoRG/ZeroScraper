#!/usr/bin/env python
from getpass import getpass
import requests
import json
import argparse
import os
import logging

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.getenv("LOG_LEVEL", "INFO"),
)
logger = logging.getLogger(__name__)


def make_json_output(args, json_output):
    if args.output:
        json.dump(json_output, open(args.output, "w"))
    else:
        print(json.dumps(json_output))


def load_token():
    try:
        access_token = json.load(open("secrets.json"))["access_token"]
    except FileNotFoundError:
        logger.exception("Cannot find secrets.json. Please login first.")
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers


def login():
    username = input("username: ")
    password = getpass("password: ")
    user_credential = {"username": username, "password": password}

    r = requests.post(os.getenv("API_URL") + "/login", data=user_credential)
    if r.status_code == 200:
        logger.info("Login successful. ")
        token = {"access_token": r.json()["access_token"]}
        json.dump(token, open("secrets.json", "w"))
    else:
        logger.info(f"Login failed. Message: {r.json()['message']}")


def stats(args):
    headers = load_token()
    if args.site_id:
        r = requests.get(
            f'{os.getenv("API_URL")}/stats?site_id={args.site_id}', headers=headers
        )
    elif args.date:
        r = requests.get(
            f'{os.getenv("API_URL")}/stats?date={args.date}', headers=headers
        )
    else:
        r = requests.get(f'{os.getenv("API_URL")}/stats', headers=headers)

    total = 0
    result = r.json()["result"]
    for s in result:
        total += s["new_article_count"] + s["updated_article_count"]

    make_json_output(args, {"total": total, "result": result})


def variables(args):
    headers = load_token()
    if args.key:
        r = requests.get(
            f'{os.getenv("API_URL")}/variables?key={args.key}', headers=headers
        )
    else:
        r = requests.get(f'{os.getenv("API_URL")}/variables', headers=headers)
    make_json_output(args, r.json()["result"])


def main(args):
    if args.command == "login":
        login()
    elif args.command == "stats":
        stats(args)
    elif args.command == "variables":
        variables(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title="sub command", dest="command", required=True)
    login_cmd = cmds.add_parser("login", help="log in to api")

    stats_cmd = cmds.add_parser("stats", help="get stats from api")
    stats_cmd.add_argument(
        "--site-id", type=int, help="retrieve stats of a particular site", nargs="?"
    )
    stats_cmd.add_argument(
        "--date", type=str, help="retrieve stats of a particular date"
    )
    stats_cmd.add_argument("-o", "--output", type=str, help="output filename")

    variable_cmd = cmds.add_parser("variables", help="get variable from api")
    variable_cmd.add_argument("--key", type=str, help="the key of variable to retrieve")
    variable_cmd.add_argument("-o", "--output", type=str, help="output filename")

    args = parser.parse_args()
    main(args)

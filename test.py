import pugsql
import os
import time
import json
import sys

print("start")


def get_last_comment_floor(queries, post):
    try:
        last_snapshot_raw_data = queries.get_post_latest_snapshot(
            article_id=post["article_id"]
        )["raw_data"]
    except TypeError:
        return 0

    last_snapshot_comments = json.loads(last_snapshot_raw_data)["comments"]
    if len(last_snapshot_comments) == 0:
        return 0
    elif "floor" not in last_snapshot_comments[-1]:
        return 0
    else:
        return last_snapshot_comments[-1]["floor"]


queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))
start = int(time.time())
posts_to_update = [
    {**post, "last_comment_floor": get_last_comment_floor(queries, post)}
    for post in queries.get_one_dcard_site_posts_to_update(
        site_id=2922, current_time=int(time.time())
    )
]
print(f"# of posts = {len(posts_to_update)}")
print(f"total time: {int(time.time())-start}")

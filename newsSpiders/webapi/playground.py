import json
import random
import time

from flask import request


def get_random_title(queries):
    titles = list(queries.get_titles(limit=10))
    body = random.choice(titles)
    return {"body": body}


def pass_verification(queries, record):
    if not isinstance(record, dict):
        return False

    publication_id = record.get("publication_id", None)
    tokens = record.get("tokens", None)
    if not tokens or not publication_id:
        return False

    if not isinstance(tokens, list) or not isinstance(publication_id, str):
        return False

    if not queries.get_title_by_id(publication_id=publication_id):
        return False

    for t in tokens:
        if {"text", "pos", "sentiment"} - t.keys():
            return False

        if not all(t.values()):
            return False

        if not set(map(type, t.values())) == {str}:
            return False

    else:
        return True


def add_record(queries):
    record = request.get_json()
    now = int(time.time())
    if pass_verification(queries, record):
        queries.update_publication_play_time(
            publication_id=record["publication_id"], last_play_at=now
        )

        queries.insert_record(
            publication_id=record["publication_id"],
            content=json.dumps(record["tokens"]),
            play_at=now,
        )

        body = {
            "message": "Add new record successfully.",
            "record": {**record, "play_at": now},
        }
        return {"body": body}
    else:
        body = {"message": "invalid record.", "record": record}
        return {"body": body, "status_code": 400}

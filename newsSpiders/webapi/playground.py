import json
import random
import time

from flask import request


def get_random_title(queries):
    titles = list(queries.get_titles(limit=10))
    body = random.choice(titles)
    return {'body': body}


def add_record(queries):
    data = request.json
    now = int(time.time())
    # todo: verify
    #      ...

    # if verification succeeded
    record_id = queries.insert_record(publication_id=data["publication_id"],
                                      content=json.dumps(data["tokens"]),
                                      play_at=now)

    queries.update_publication_play_time(publication_id=data["publication_id"],
                                         last_play_at=now)

    body = {'status': 'good', 'message': 'add new record successfully.', 'record_id': record_id}
    return {'body': body}

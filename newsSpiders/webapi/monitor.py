import time
from datetime import timedelta
from flask import request


def check_health(queries):
    latest_snapshot_at = queries.get_max_snapshot_at()["max_snapshot_at"]
    now = int(time.time())
    if latest_snapshot_at > now - int(timedelta(minutes=15).total_seconds()):
        body = 'okay'
    else:
        body = 'not okay'

    return {'body': body}


def get_variable(queries):
    key = request.args.get("key")
    body = queries.get_variable(key=key)

    return {'body': body}

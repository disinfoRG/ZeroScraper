import time
from datetime import timedelta


def check_health(queries):
    latest_snapshot_at = queries.get_max_snapshot_at()["max_snapshot_at"]
    now = int(time.time())
    if latest_snapshot_at > now - int(timedelta(minutes=15).total_seconds()):
        body = "okay"
    else:
        body = "not okay"

    return {"body": body}


def get_variables(queries, args):
    status_code = 200
    key = args.get("key", None)
    if not key:
        result = list(queries.get_all_variables())
        response_body = {"message": "returning all variables", "result": result}
    else:
        result = queries.get_variable_by_key(key=key)
        if result:
            response_body = {
                "message": f"returning variables with key {key}",
                "result": result,
            }
        else:
            response_body = {"message": f"key {key} does not exist.", "result": dict()}
            status_code = 404

    return {"body": response_body, "status_code": status_code}

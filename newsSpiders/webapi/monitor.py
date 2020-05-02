import time
from datetime import timedelta


def find_earlier_time(minutes):
    now = int(time.time())
    return now - int(timedelta(minutes=minutes).total_seconds())


def check_health(queries):
    counts = queries.count_recent_articles_by_process(
        after=find_earlier_time(minutes=30)
    )
    result = {}
    for key in counts.keys():
        if counts[key] > 0:
            result[key] = "okay"
        else:
            result[key] = "not okay"

    return {"body": result}


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

import requests


def search_publication(search_url, args):
    search_string = args.get("q", None)
    if not search_string:
        return {
            "body": {"message": "Please provide a search string.", "result": list()},
            "status_code": 400,
        }

    r = requests.get(
        f"{search_url}/_search?q={search_string}&filter_path=hits.hits._source"
    )
    result = [x["_source"] for x in r.json()["hits"]["hits"]]
    return {
        "body": {
            "message": f"Return publications that matches {search_string}",
            "result": result,
        }
    }

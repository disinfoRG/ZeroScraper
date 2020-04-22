from flask import request
from url_normalize import url_normalize


def get_article_by_id(queries, article_id):
    body = queries.get_article_by_id(article_id=article_id)
    return {"body": body}


def get_article_by_url(queries):
    url = request.args.get("url", None)
    normalized_url = url_normalize(url)

    if url is None:
        body = {"message": "please provide a valid url as params"}
        return {"body": body, "status_code": 404}

    body = list(queries.get_article_by_url(url=normalized_url))

    return {"body": body}

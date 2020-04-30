from url_normalize import url_normalize
import zlib


def get_article_by_id(queries, article_id):
    result = queries.get_article_by_id(article_id=article_id)
    if result:
        return {
            "body": {
                "message": f"Returning article with id {article_id}",
                "result": result,
            }
        }
    else:
        return {
            "body": {"message": f"No article with id {article_id}", "result": {}},
            "status_code": 404,
        }


def get_articles(queries, args):
    status_code = 200
    url = args.get("url", None)

    if url:
        normalized_url = url_normalize(url)
        url_hash = str(zlib.crc32(normalized_url.encode()))
        result = list(queries.get_article_by_url(url=normalized_url, url_hash=url_hash))
        if result:
            response_body = {
                "message": f"Returning articles that matches url {normalized_url}",
                "result": result,
            }
        else:
            response_body = {
                "message": f"No article matches url {normalized_url}",
                "result": list(),
            }
            status_code = 404
    else:
        result = list(queries.get_recent_articles(limit=10))
        response_body = {
            "message": "Returning 10 most recent articles.",
            "result": result,
        }

    return {"body": response_body, "status_code": status_code}

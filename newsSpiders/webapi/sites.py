from url_normalize import url_normalize


def get_sites(queries, args):
    status_code = 200
    url = args.get("url", None)
    if url:
        normalized_url = url_normalize(url)
        result = queries.get_site_by_url(url=normalized_url)
        if result:
            response_body = {
                "message": f"Returning site with url '{normalized_url}'",
                "result": result,
            }
        else:
            response_body = {
                "message": f"No site having url '{normalized_url}'",
                "result": {},
            }
            status_code = 404

    else:
        result = list(queries.get_all_sites())
        response_body = {"message": "Returning all sites", "result": result}
    return {"body": response_body, "status_code": status_code}


def get_site_by_id(queries, site_id):
    status_code = 200
    result = queries.get_site_by_id(site_id=site_id)
    if result:
        response_body = {
            "message": f"Returning site with id {site_id}",
            "result": result,
        }
    else:
        response_body = {"message": f"No site with id {site_id}", "result": {}}
        status_code = 404

    return {"body": response_body, "status_code": status_code}


def get_active_sites(queries):
    return {
        "body": {
            "message": "Returning active sites",
            "result": list(queries.get_active_sites()),
        }
    }


def get_article_count(queries, site_id):
    site = queries.get_site_by_id(site_id=site_id)
    if site:
        article_count = queries.get_site_article_count(site_id=site_id)["article_count"]
        return {
            "body": {
                "message": f"Returning article count of site {site_id}",
                "result": {"site": site, "article_count": article_count},
            }
        }
    else:
        return {
            "body": {"message": f"No site with id {site_id}", "result": {}},
            "status_code": 404,
        }


def get_latest_article(queries, site_id):
    site = queries.get_site_by_id(site_id=site_id)
    if site:
        latest_article = queries.get_site_latest_article(site_id=site_id)
        return {
            "body": {
                "message": f"Returning latest article from site {site_id}",
                "result": {"site": site, "latest_article": latest_article},
            }
        }

    else:
        return {
            "body": {"message": f"No site with id {site_id}", "result": {}},
            "status_code": 404,
        }

import math


def get_publication_count(queries, search_string):
    print("retrieving count...")
    query = f"%{search_string}%"
    pub_count = queries.get_publication_count_by_like(query=query)["publication_count"]
    return pub_count


def get_publication(queries, search_string):
    query = f"%{search_string}%"
    pubs = list(queries.get_publication_by_like(query=query))
    return pubs


def paginate(publications, page_requested, limit):
    # make response
    result = dict()
    publication_count = len(publications)
    total_page = math.ceil(publication_count / limit)
    start = (page_requested - 1) * 20
    end = min(publication_count, start + limit)

    if publication_count == 0:
        return {"error_message": f"No publication found."}, 404

    if page_requested > total_page:
        return (
            {
                "error_message": f"There are {total_page} pages of results, please specify a valid page."
            },
            404,
        )

    if page_requested < 1:
        return (
            {
                "error_message": f"unknown page {page_requested}, please specify a valid page."
            },
            404,
        )

    result["page_count"] = total_page
    result["total_publication_count"] = publication_count
    result["current_page"] = page_requested
    result["current_page_publication_count"] = end - start
    result["publications"] = publications[start:end]

    return result, 200

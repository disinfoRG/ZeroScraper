import requests
from url_normalize import url_normalize
from assert_functions import assert_valid_response, assert_invalid_response
from values import api_url, auth_header, ArticlesValues as V


def test_not_authorized():
    r = requests.get(api_url + f"/articles")
    assert r.status_code == 401


def test_route():
    r = requests.get(api_url + f"/articles", headers=auth_header)
    assert_valid_response(r, V.result_fields)
    assert len(r.json()["result"]) == 10


def test_existing_id():
    article_id = V.existing_article_id
    r = requests.get(api_url + f"/articles/{article_id}", headers=auth_header)
    assert_valid_response(r, V.result_fields, dict_result=True)


def test_nonexisting_id():
    article_id = V.nonexisting_article_id
    r = requests.get(api_url + f"/articles/{article_id}", headers=auth_header)
    assert_invalid_response(r)


def test_existing_urls():
    urls = V.existing_urls
    for u in urls:
        r = requests.get(api_url + f"/articles?url={u}", headers=auth_header)
        assert_valid_response(r, V.result_fields)
        for article in r.json()["result"]:
            normalized_u = url_normalize(u)
            assert (
                article["url"] == normalized_u or article["redirect_to"] == normalized_u
            )


def test_nonexisting_urls():
    urls = V.nonexisting_urls
    for u in urls:
        r = requests.get(api_url + f"/articles?url={u}", headers=auth_header)
        assert_invalid_response(r)

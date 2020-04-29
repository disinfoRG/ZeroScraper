import requests
from assert_functions import assert_valid_response, assert_invalid_response
from url_normalize import url_normalize
from values import api_url, auth_header, ArticlesValues


def test_not_authorized():
    r = requests.get(api_url + f"/articles")
    assert r.status_code == 401


def test_route():
    r = requests.get(api_url + f"/articles", headers=auth_header)
    assert_valid_response(r, ArticlesValues.result_fields)
    assert len(r.json()["result"]) <= 10


def test_existing_id():
    article_id = ArticlesValues.existing_article_id
    r = requests.get(api_url + f"/articles/{article_id}", headers=auth_header)
    assert_valid_response(r, ArticlesValues.result_fields, dict_result=True)


def test_nonexisting_id():
    article_id = ArticlesValues.nonexisting_article_id
    r = requests.get(api_url + f"/articles/{article_id}", headers=auth_header)
    assert_invalid_response(r)


def test_existing_urls():
    urls = ArticlesValues.existing_urls
    for u in urls:
        r = requests.get(api_url + f"/articles?url={u}", headers=auth_header)
        assert_valid_response(r, ArticlesValues.result_fields)
        for article in r.json()["result"]:
            normalized_u = url_normalize(u)
            assert (
                article["url"] == normalized_u or article["redirect_to"] == normalized_u
            )


def test_nonexisting_urls():
    urls = ArticlesValues.nonexisting_urls
    for u in urls:
        r = requests.get(api_url + f"/articles?url={u}", headers=auth_header)
        assert_invalid_response(r)

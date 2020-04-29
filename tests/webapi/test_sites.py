import requests
from values import api_url, auth_header, SitesValues
from assert_functions import assert_valid_response, assert_invalid_response


def test_not_authorized():
    r = requests.get(api_url + f"/sites")
    assert r.status_code == 401


def test_route():
    r = requests.get(api_url + f"/sites", headers=auth_header)
    assert_valid_response(r, SitesValues.result_fields)


def test_get_active_sites():
    r = requests.get(api_url + f"/sites/active", headers=auth_header)
    assert_valid_response(r, SitesValues.result_fields)
    assert {x["is_active"] for x in r.json()["result"]} == {1}


def test_existing_site_id():
    site_id = SitesValues.existing_site_id
    r = requests.get(api_url + f"/sites/{site_id}", headers=auth_header)
    assert_valid_response(r, SitesValues.result_fields, dict_result=True)

    r = requests.get(api_url + f"/sites/{site_id}/article_count", headers=auth_header)
    assert_valid_response(r, result_fields={"site", "article_count"}, dict_result=True)
    result = r.json()["result"]
    assert isinstance(result["article_count"], int)
    assert isinstance(result["site"], dict)

    r = requests.get(api_url + f"/sites/{site_id}/latest_article", headers=auth_header)
    assert_valid_response(r, result_fields={"site", "latest_article"}, dict_result=True)
    result = r.json()["result"]
    assert isinstance(result["latest_article"], dict)
    assert isinstance(result["site"], dict)


def test_nonexisting_site_id():
    site_id = SitesValues.nonexisting_site_id
    r = requests.get(api_url + f"/sites/{site_id}", headers=auth_header)
    assert_invalid_response(r)

    r = requests.get(api_url + f"/sites/{site_id}/article_count", headers=auth_header)
    assert_invalid_response(r)

    r = requests.get(api_url + f"/sites/{site_id}/latest_article", headers=auth_header)
    assert_invalid_response(r)

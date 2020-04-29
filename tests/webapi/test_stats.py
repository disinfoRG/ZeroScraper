import requests
from assert_functions import assert_valid_response, assert_invalid_response
from values import api_url, auth_header, StatsValues


def test_not_authorized():
    r = requests.get(api_url + f"/stats")
    assert r.status_code == 401


def test_route():
    r = requests.get(api_url + f"/stats", headers=auth_header)
    assert_valid_response(r, StatsValues.result_fields)


def test_existing_site():
    site_id = StatsValues.existing_site_id

    r = requests.get(api_url + f"/stats?site_id={site_id}", headers=auth_header)
    assert_valid_response(r, StatsValues.result_fields)
    assert len(r.json()["result"]) <= 30
    assert set([x["site_id"] for x in r.json()["result"]]) == {site_id}


def test_date_with_stats():
    date = StatsValues.date_with_stats
    r = requests.get(api_url + f"/stats?date={date}", headers=auth_header)
    assert_valid_response(r, StatsValues.result_fields)
    assert set([x["date"] for x in r.json()["result"]]) == {date}


def test_date_without_stats():
    date = StatsValues.date_without_stats
    r = requests.get(api_url + f"/stats?date={date}", headers=auth_header)
    assert_invalid_response(r)


def test_invalid_date():
    date = StatsValues.invalid_date
    r = requests.get(api_url + f"/stats?date={date}", headers=auth_header)
    assert_invalid_response(r)

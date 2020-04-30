import requests
from values import api_url, AuthValues as V


def test_login():
    r = requests.post(api_url + f"/login?username={V.username}&password={V.password}")
    assert r.status_code == 200
    assert {"message", "access_token"} == r.json().keys()
    assert r.json()["access_token"]
    r = requests.get(
        api_url, headers={"Authorization": "Bearer " + r.json()["access_token"]}
    )
    assert V.username in r.text

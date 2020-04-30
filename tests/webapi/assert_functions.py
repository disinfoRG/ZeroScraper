def assert_valid_response(r, result_fields, dict_result=False):
    response = r.json()
    assert r.status_code == 200
    assert isinstance(response, dict)
    assert response.keys() == {"message", "result"}
    if dict_result:
        assert isinstance(response["result"], dict)
        assert bool(result_fields - response["result"].keys()) is False
    else:
        assert isinstance(response["result"], list)
        assert bool(result_fields - response["result"][0].keys()) is False


def assert_invalid_response(r):
    assert r.status_code == 404
    assert set(r.json().keys()) == {"message", "result"}
    assert bool(r.json()["result"]) is False

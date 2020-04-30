import json
import time

import pugsql
import requests
from values import api_url, PlaygroundValues as V


def test_get_random_title():
    r = requests.get(api_url + "/playground/random")
    assert r.status_code == 200
    assert r.json().keys() == {"text", "publication_id"}


def test_post_invalid_record():
    for record in V.invalid_records:
        r = requests.post(api_url + "/playground/add_record", json=record)
        time.sleep(0.2)
        assert r.status_code == 400


def test_post_valid_record():
    queries = pugsql.module("tests/webapi/queries")
    queries.connect(V.PLAY_DB_URL)

    for record in V.valid_records:
        original_publication = queries.get_publication_by_id(
            publication_id=record["publication_id"]
        )
        r = requests.post(api_url + "playground/add_record", json=record)
        assert r.status_code == 200
        assert r.json()["record"]
        inserted_record = queries.get_record(
            publication_id=record["publication_id"],
            play_at=r.json()["record"]["play_at"],
        )
        assert inserted_record
        assert json.loads(inserted_record["content"]) == record["tokens"]

        updated_publication = queries.get_publication_by_id(
            publication_id=record["publication_id"]
        )
        assert updated_publication["last_play_at"] > (
            original_publication["last_play_at"] or 0
        )
        assert (
            updated_publication["play_count"] == original_publication["play_count"] + 1
        )

    queries.disconnect()

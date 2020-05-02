import json
import os

import dotenv

dotenv.load_dotenv()

auth_header = {
    "Authorization": f'Bearer {json.load(open("secrets.json"))["access_token"]}'
}
api_url = os.getenv("API_URL")


class AuthValues:
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")


class MonitorValues:
    variable_fields = {"key", "value"}
    variable_tests = [
        {"key": "test:pid", "value": "12345"},
        {"key": "test2:pid", "value": "789"},
    ]
    health_fields = {"discover", "update"}


class StatsValues:
    result_fields = {"site_id", "date", "new_article_count", "updated_article_count"}
    existing_site_id = 98
    nonexisting_site_id = 0
    date_with_stats = "2020-03-01"
    date_without_stats = "2020-02-20"
    invalid_date = "xxx"


class ArticlesValues:
    result_fields = {
        "article_id",
        "site_id",
        "url",
        "snapshot_count",
        "first_snapshot_at",
        "last_snapshot_at",
    }
    existing_article_id = 3777556
    nonexisting_article_id = 0
    existing_urls = [
        "tw.appledaily.com/finance/realtime/20200415/1731812/",
        "http://www.tailian.org.cn/gdtl/201604/t20160426_11444102.htm",
    ]
    nonexisting_urls = ["www.google.com"]


class SitesValues:
    result_fields = {"is_active", "url", "site_id", "name"}
    existing_site_id = 105
    nonexisting_site_id = 0


class PlaygroundValues:
    TEST_PLAY_DB_URL = os.getenv("PLAY_DB_URL")
    invalid_records = [
        None,
        list(),
        dict(),
        {"id": "123", "whatever": "456"},
        {"publication_id": None, "tokens": []},
        {"publication_id": "000133F4825411EA8627F23C92E71BAD", "tokens": []},
        {"publication_id": "000133F4825411EA8627F23C92E71BAD", "tokens": None},
        {
            "publication_id": 123,
            "tokens": [{"text": "123", "sentiment": "456", "pos": "123"}],
        },
        {
            "publication_id": "000133F4825411EA8627F23C92E71BAD",
            "tokens": [{"text": "123", "sentiment": 123, "pos": "123"}],
        },
        {
            "publication_id": "000133F4825411EA8627F23C92E71BAD",
            "tokens": [{"text": "123", "sentiment": "123", "pos": ""}],
        },
        {
            "publication_id": "000133F4825411EA8627F23C92E71BAD",
            "tokens": [{"text": "123", "sentiment": "123", "pos": None}],
        },
        {
            "publication_id": "000133F4825411EA8627F23C92E71BAD",
            "tokens": [{"text": "1", "sentiment": "123", "pos": "123"}, {"text": "1"}],
        },
        {
            "publication_id": "123test",
            "tokens": [{"text": "1", "sentiment": "123", "pos": "123"}],
        },
    ]

    valid_records = [
        {
            "publication_id": "000133F4825411EA8627F23C92E71BAD",
            "tokens": [
                {"text": "228", "sentiment": "中", "pos": "名"},
                {"text": "連假", "sentiment": "中", "pos": "名"},
                {"text": "前夕", "sentiment": "中", "pos": "形"},
            ],
        }
    ]

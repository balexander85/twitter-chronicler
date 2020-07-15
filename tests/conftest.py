"""conftest.py"""
from typing import List, Union

import pytest
from twitter import Status, User, Url

from config import TEST_JSON_FILE
from util import fetch_test_data_file


def convert_dicts_in_status_to_obj(status: Status) -> Status:
    """Update each attribute of status with Twitter object"""
    keys_to_update = ["urls", "user", "user_mentions", "quoted_status"]
    for key in keys_to_update:
        if key == "urls":
            status.urls = [Url(**url) for url in status.__getattribute__(key)]
        elif key == "user":
            status.user = User(**status.__getattribute__(key))
        elif key == "user_mentions":
            status.user_mentions = [
                User(**user) for user in status.__getattribute__(key)
            ]
        elif key == "quoted_status":
            status.quoted_status = (
                convert_dicts_in_status_to_obj(
                    status=Status(**status.__getattribute__(key))
                )
                if status.__getattribute__(key)
                else None
            )
    return status


def generate_mock_tweet(
    raw_status: Union[Status, List[Status]]
) -> Union[Status, List[Status]]:
    """Return mocked tweet to be used in tests"""
    if type(raw_status) == list:
        updated_status = [
            generate_mock_tweet(raw_status=status) for status in raw_status
        ]
    else:
        updated_status = convert_dicts_in_status_to_obj(status=raw_status)

    return updated_status


def fetch_test_data(data_name):
    json_file = fetch_test_data_file(file=TEST_JSON_FILE)

    if type(json_file.get(data_name)) is list:
        return generate_mock_tweet(
            raw_status=[Status(**s) for s in json_file.get(data_name)]
        )
    else:
        return generate_mock_tweet(raw_status=Status(**json_file.get(data_name)))


@pytest.fixture(name="test_status")
def get_test_status():
    def _get_status(key_name):
        return fetch_test_data(key_name)

    return _get_status

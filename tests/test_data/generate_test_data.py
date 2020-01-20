import json
from typing import List, Union

from twitter import Status, Url, User

from config import TEST_JSON_FILE_NAME

# from twitter_helpers import twitter_api
# tweet = twitter_api.GetStatus(status_id=1206058311864528896)

with open(TEST_JSON_FILE_NAME, "r") as f:
    json_file = json.load(f)


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


test_tweet = {
    "basic_tweet": generate_mock_tweet(
        raw_status=Status(**json_file.get("basic_tweet"))
    ),
    "quoted_tweet": generate_mock_tweet(
        raw_status=Status(**json_file.get("quoted_tweet"))
    ),
    "mock_status": generate_mock_tweet(
        raw_status=[Status(**s) for s in json_file.get("mocked_status")]
    ),
}

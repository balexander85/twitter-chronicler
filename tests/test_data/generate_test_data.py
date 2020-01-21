import json
from typing import List, Union

from twitter import Status, Url, User

from config import TEST_JSON_FILE_NAME, TEMP_JSON_FILE_NAME


def save_user_test_data(file_name, user_name, count):
    """Make call with twitter api to get test data"""
    from twitter_helpers import twitter_api

    tweets = twitter_api.GetUserTimeline(screen_name=user_name, count=count)
    clean_tweets = [s.AsDict() for s in tweets]
    with open(file_name, "w") as f:
        for t in clean_tweets:
            json.dump(t, f)


def save_tweet_test_data(file_name, status):
    """Make call with twitter api to get test data"""
    from twitter_helpers import twitter_api

    tweet = twitter_api.GetStatus(status_id=status)
    with open(file_name, "w") as f:
        json.dump(tweet.AsDict(), f)


def fetch_test_data(data_name):
    with open(TEST_JSON_FILE_NAME, "r") as f:
        json_file = json.load(f)

    if type(json_file.get(data_name)) is list:
        return generate_mock_tweet(
            raw_status=[Status(**s) for s in json_file.get(data_name)]
        )
    else:
        return generate_mock_tweet(raw_status=Status(**json_file.get(data_name)))


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


if __name__ == "__main__":
    # uncomment when ready to save test data
    # save_tweet_test_data(TEMP_JSON_FILE_NAME, 1218672858513190913)
    pass

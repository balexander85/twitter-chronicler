import json
from typing import Iterator

from _logger import LOGGER


def fetch_test_data_file(file_name: str):
    with open(file_name, "r") as f:
        json_file = json.load(f)
    return json_file


def file_reader(file_name: str) -> Iterator[str]:
    """Yield entries from files"""
    for row in open(file_name, "r"):
        clean_row = row.strip("\n")
        yield clean_row


def add_status_id_to_file(tweet_id: str, list_of_ids_replied_to_file_name: str):
    """Save id of the replied to tweet

    Save id to file so that tweet will not be replied to more than once.
    """
    DeprecationWarning(
        "add_status_id_to_file has been deprecated, "
        "please use add_status_id_to_file_new"
    )
    add_status_id_to_file_new(
        tweet_id=tweet_id, user_status_file=list_of_ids_replied_to_file_name
    )


def add_status_id_to_file_new(tweet_id: str, user_status_file: str):
    """Save id of the replied to tweet

    Save id to file so that tweet will not be replied to more than once.
    """
    LOGGER.debug(msg=f"Adding {tweet_id} to {user_status_file}")
    with open(user_status_file, "a+") as f:
        f.write(tweet_id + "\n")

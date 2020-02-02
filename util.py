from typing import Iterator

from _logger import LOGGER


def file_reader(file_name: str) -> Iterator[str]:
    """Yield entries from files"""
    for row in open(file_name, "r"):
        clean_row = row.strip("\n")
        yield clean_row


def add_status_id_to_file(tweet_id: str, list_of_ids_replied_to_file_name: str):
    """Save id of the replied to tweet

    Save id to file so that tweet will not be replied to more than once.
    """
    LOGGER.debug(msg=f"Adding {tweet_id} to {list_of_ids_replied_to_file_name}")
    with open(list_of_ids_replied_to_file_name, "a+") as f:
        f.write(tweet_id + "\n")

import json
from pathlib import Path, PosixPath
from typing import Iterator

from _logger import get_module_logger

LOGGER = get_module_logger(__name__)


def fetch_test_data_file(file: PosixPath):
    with file.open() as f:
        json_file = json.load(f)
    return json_file


def file_reader(file: PosixPath) -> Iterator[str]:
    """Yield entries from files"""
    for row in file.open():
        clean_row = row.strip("\n")
        yield clean_row


def add_status_id_to_file(tweet_id: str, list_of_ids_replied_to_file_name: str):
    """Save id of the replied to tweet

    Save id to file so that tweet will not be replied to more than once.
    """
    DeprecationWarning(
        "add_status_id_to_file has been deprecated, please use add_line_to_file"
    )
    add_line_to_file(line=tweet_id, file_path=list_of_ids_replied_to_file_name)


def add_status_id_to_file_new(tweet_id: str, user_status_file: str):
    """Save id of the replied to tweet

    Save id to file so that tweet will not be replied to more than once.
    """
    DeprecationWarning(
        "add_status_id_to_file_new has been deprecated, please use add_line_to_file"
    )
    add_line_to_file(line=tweet_id, file_path=user_status_file)


def add_line_to_file(line: str, file_path: str):
    """Append line to file and add new line"""
    LOGGER.debug(msg=f"Adding {line} to {file_path}")
    with Path(file_path).open(mode="a+") as f:
        f.write(line + "\n")

from configparser import ConfigParser
from typing import Iterator, List
import os

from util import file_reader

PROJECT_DIR_PATH = os.path.dirname(__file__)


config = ConfigParser()
config.read(os.path.join(PROJECT_DIR_PATH, "config.ini"))

# Twitter API config
APP_KEY = config.get("default", "APP_KEY")
APP_SECRET = config.get("default", "APP_SECRET")
OAUTH_TOKEN = config.get("default", "OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = config.get("default", "OAUTH_TOKEN_SECRET")

# Selenium config
CHROME_DRIVER_PATH = config.get("default", "CHROME_DRIVER_PATH")

# General config
LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME: str = os.path.join(
    PROJECT_DIR_PATH, "list_of_status_ids_replied_to.txt"
)
LIST_OF_USERS_TO_FOLLOW_FILE_NAME: str = os.path.join(
    PROJECT_DIR_PATH, "list_of_users_to_follow.txt"
)
# LIST_OF_USERS_TO_FOLLOW: Iterator[str] = file_reader(LIST_OF_USERS_TO_FOLLOW_FILE_NAME)
# LIST_OF_STATUS_IDS_REPLIED_TO: Iterator[str] = file_reader(
#     LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME
# )

with open(LIST_OF_USERS_TO_FOLLOW_FILE_NAME, "r") as follower_file:
    LIST_OF_USERS_TO_FOLLOW: List[str] = [
        line.strip("\n") for line in follower_file.readlines()
    ]

with open(LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME, "r") as f:
    LIST_OF_STATUS_IDS_REPLIED_TO: List[str] = [
        line.strip("\n") for line in f.readlines()
    ]

# Test config
TEST_JSON_FILE_NAME: str = os.path.join(PROJECT_DIR_PATH, "tests/test_data/status.json")
TWITTER_API_USER = {"screen_name": "FTBandFTR"}
TWITTER_URL = "https://twitter.com"

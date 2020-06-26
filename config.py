from configparser import ConfigParser
from typing import List
import os

PROJECT_DIR_PATH = os.path.dirname(__file__)


config = ConfigParser()
config.read(os.path.join(PROJECT_DIR_PATH, "conf", "config.ini"))

# Twitter API config
APP_KEY = config.get("default", "APP_KEY")
APP_SECRET = config.get("default", "APP_SECRET")
OAUTH_TOKEN = config.get("default", "OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = config.get("default", "OAUTH_TOKEN_SECRET")

# Selenium config
CHROME_DRIVER_PATH = config.get("default", "CHROME_DRIVER_PATH")

# General config
LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME: str = os.path.join(
    PROJECT_DIR_PATH, "conf", "list_of_status_ids_replied_to.txt"
)
LIST_OF_USERS_TO_FOLLOW_FILE_NAME: str = os.path.join(
    PROJECT_DIR_PATH, "conf", "list_of_users_to_follow.txt"
)

with open(LIST_OF_USERS_TO_FOLLOW_FILE_NAME, "r") as follower_file:
    followers = follower_file.readlines()
    LIST_OF_USERS_TO_FOLLOW: List[str] = list(
        map(
            lambda line: line.strip("\n"),
            filter(
                lambda line: not line.startswith("#") and line.strip("\n"), followers
            ),
        )
    )

with open(LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME, "r") as f:
    LIST_OF_STATUS_IDS_REPLIED_TO: List[str] = [
        line.strip("\n") for line in f.readlines()
    ]

# Test config
TEST_JSON_FILE_NAME: str = os.path.join(PROJECT_DIR_PATH, "tests/test_data/status.json")
TEMP_JSON_FILE_NAME: str = os.path.join(
    PROJECT_DIR_PATH, "tests/test_data/temp_status.json"
)
TWITTER_API_USER = {"screen_name": "FTBandFTR"}
TWITTER_URL = "https://twitter.com"

from configparser import ConfigParser
from pathlib import Path, PosixPath
from typing import List

PROJECT_DIR_PATH = Path(__file__).parent


config = ConfigParser()
config.read(PROJECT_DIR_PATH.joinpath("conf", "config.ini"))

# Twitter API config
APP_KEY = config.get("default", "APP_KEY")
APP_SECRET = config.get("default", "APP_SECRET")
OAUTH_TOKEN = config.get("default", "OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = config.get("default", "OAUTH_TOKEN_SECRET")

# Twitter API config for user that scans tweets
READ_APP_KEY = config.get("default", "READ_APP_KEY")
READ_APP_SECRET = config.get("default", "READ_APP_SECRET")
READ_OAUTH_TOKEN = config.get("default", "READ_OAUTH_TOKEN")
READ_OAUTH_TOKEN_SECRET = config.get("default", "READ_OAUTH_TOKEN_SECRET")
# Twitter API config for user that replies with screenshot
WRITE_APP_KEY = config.get("default", "WRITE_APP_KEY")
WRITE_APP_SECRET = config.get("default", "WRITE_APP_SECRET")
WRITE_OAUTH_TOKEN = config.get("default", "WRITE_OAUTH_TOKEN")
WRITE_OAUTH_TOKEN_SECRET = config.get("default", "WRITE_OAUTH_TOKEN_SECRET")

# Selenium config
CHROME_DRIVER_PATH = config.get("default", "CHROME_DRIVER_PATH")

# General config
LIST_OF_STATUS_IDS_REPLIED_TO_FILE: PosixPath = PROJECT_DIR_PATH.joinpath(
    "conf", "list_of_status_ids_replied_to.txt"
)
LIST_OF_USERS_TO_FOLLOW_FILE: PosixPath = PROJECT_DIR_PATH.joinpath(
    "conf", "list_of_users_to_follow.txt"
)

CHECKED_STATUSES_DIR_PATH: PosixPath = PROJECT_DIR_PATH.joinpath(
    "conf", "statuses_checked"
)

with LIST_OF_USERS_TO_FOLLOW_FILE.open() as follower_file:
    followers = follower_file.readlines()
    LIST_OF_USERS_TO_FOLLOW: List[str] = list(
        map(
            lambda line: line.strip("\n"),
            filter(
                lambda line: not line.startswith("#") and line.strip("\n"), followers
            ),
        )
    )

with LIST_OF_STATUS_IDS_REPLIED_TO_FILE.open() as f:
    LIST_OF_STATUS_IDS_REPLIED_TO: List[str] = list(
        filter(None, map(lambda line: line.strip("\n"), f.readlines()))
    )

# Test config
TEST_JSON_FILE: PosixPath = PROJECT_DIR_PATH.joinpath(
    "tests", "test_data", "status.json"
)
TEMP_JSON_FILE: PosixPath = PROJECT_DIR_PATH.joinpath(
    "tests", "test_data", "temp_status.json"
)
TWITTER_API_USER = {"screen_name": "FTBandFTR"}
TWITTER_URL = "https://twitter.com"

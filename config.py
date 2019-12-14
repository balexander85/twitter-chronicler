from configparser import ConfigParser
from typing import List
import os

absolute_path = os.path.abspath(".")
config = ConfigParser()
config.read("config.ini")

APP_KEY = config.get("default", "APP_KEY")
APP_SECRET = config.get("default", "APP_SECRET")
OAUTH_TOKEN = config.get("default", "OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = config.get("default", "OAUTH_TOKEN_SECRET")

CHROME_DRIVER_PATH = config.get("default", "CHROME_DRIVER_PATH")

LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME = os.path.join(
    absolute_path, "list_of_status_ids_replied_to.txt"
)
LIST_OF_USERS_TO_FOLLOW_FILE_NAME = os.path.join(
    absolute_path, "list_of_users_to_follow.txt"
)

with open(LIST_OF_USERS_TO_FOLLOW_FILE_NAME, "r") as follower_file:
    LIST_OF_USERS_TO_FOLLOW: List[str] = [
        line.strip("\n") for line in follower_file.readlines()
    ]

with open(LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME, "r") as f:
    LIST_OF_STATUS_IDS_REPLIED_TO: List[str] = [
        line.strip("\n") for line in f.readlines()
    ]

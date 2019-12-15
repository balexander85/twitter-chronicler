import logging
import os
from sys import stdout
from typing import List

from twitter import Api as twitterApi
from twitter import Status

from config import (
    APP_KEY,
    APP_SECRET,
    LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME,
    PROJECT_DIR_PATH,
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    stream=stdout,
)
LOGGER = logging.getLogger(__name__)


twitter_api = twitterApi(
    consumer_key=APP_KEY,
    consumer_secret=APP_SECRET,
    access_token_key=OAUTH_TOKEN,
    access_token_secret=OAUTH_TOKEN_SECRET,
)


class Tweet:
    def __init__(self, tweet: Status):
        self.raw_tweet = tweet
        self.id: int = self.raw_tweet.id
        self.id_str: str = self.raw_tweet.id_str
        self.tweet_text = self.raw_tweet.text
        self.tweet_locator = f"div[data-tweet-id='{self.id}']"
        self.user: str = self.raw_tweet.user.screen_name
        self.quoted_status = self.raw_tweet.quoted_status
        self.quoted_tweet_id: str = self.quoted_status.id
        self.quoted_tweet_locator = f"div[data-tweet-id='{self.quoted_tweet_id}']"

    def __repr__(self):
        return f"@{self.user}: {self.tweet_text}"

    @property
    def quoted_tweet_url(self) -> str:
        tweet_url = f"https://twitter.com/{self.user}/status/{self.quoted_tweet_id}"
        LOGGER.info(msg=f"{tweet_url} : {self}")
        return tweet_url

    @property
    def screen_capture_file_name_quoted_tweet(self) -> str:
        return f"tweet_capture_{self.quoted_tweet_id}.png"

    @property
    def screen_capture_file_path_quoted_tweet(self) -> str:
        return os.path.join(
            PROJECT_DIR_PATH, "screen_shots", self.screen_capture_file_name_quoted_tweet
        )

    @property
    def urls_from_quoted_tweet(self) -> List[str]:
        return [url_obj.url for url_obj in self.quoted_status.urls]


def save_status_id_of_replied_to_tweet(tweet: Tweet):
    LOGGER.info(
        msg=f"Adding {tweet.id_str} to {LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME}"
    )
    with open(LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME, "a+") as f:
        f.write(tweet.id_str + "\n")

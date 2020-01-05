import logging
import os
from sys import stdout
from typing import List

from twitter import Api as twitterApi
from twitter import Status, TwitterError

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
    """Class representing a Status (tweet)"""

    def __init__(self, tweet: Status):
        self.raw_tweet: Status = tweet
        self.id: int = self.raw_tweet.id
        self.id_str: str = self.raw_tweet.id_str
        self.tweet_text: str = self.raw_tweet.text
        self.tweet_locator: str = f"div[data-tweet-id='{self.id}']"
        self.user: str = self.raw_tweet.user.screen_name

    def __repr__(self):
        tweet = f"@{self.user}: {self.tweet_text}"
        LOGGER.debug(f"Processing '{tweet}'")
        return tweet

    @property
    def quoted_status(self) -> Status:
        """Return True if tweet quotes another"""
        return self.raw_tweet.quoted_status

    @property
    def quoted_tweet_id(self) -> str:
        """Return id of the quoted tweet"""
        if self.quoted_status:
            return self.quoted_status.id
        else:
            LOGGER.error(f"Tweet has no quoted status associated. {self}")

    @property
    def quoted_tweet_locator(self) -> str:
        """Return locator for the div of the quoted tweet"""
        return f"div[data-tweet-id='{self.quoted_tweet_id}']"

    @property
    def quoted_tweet_url(self) -> str:
        tweet_url = f"https://twitter.com/{self.user}/status/{self.quoted_tweet_id}"
        LOGGER.info(msg=f"{tweet_url} : {self}")
        return tweet_url

    @property
    def replied_to_status_bool(self) -> bool:
        """Return True if tweet quotes another"""
        return False if not self.raw_tweet.in_reply_to_status_id else True

    @property
    def replied_to_status_id(self) -> int:
        """Return True if tweet quotes another"""
        return self.raw_tweet.in_reply_to_status_id

    @property
    def replied_to_user_screen_name(self) -> str:
        """Returns screen name of the user that is being replied to"""
        return self.raw_tweet.in_reply_to_screen_name

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


def get_all_users_tweets(twitter_user: str) -> List[Tweet]:
    """Helper method to collect ALL of a user's tweets"""
    LOGGER.info(f"Getting tweets for user: {twitter_user}")
    initial_tweets = [
        Tweet(t)
        for t in twitter_api.GetUserTimeline(screen_name=twitter_user, count=200)
    ]
    last_tweet_id = initial_tweets[-1].id
    user_tweet_count = twitter_api.GetUser(screen_name=twitter_user).statuses_count
    if int(user_tweet_count) > 1000:
        raise Exception("Whatever the hourly rate limit would be raise error for now")

    for _ in range(int(user_tweet_count / 200)):
        new_tweets = [
            Tweet(t)
            for t in twitter_api.GetUserTimeline(
                screen_name=twitter_user, max_id=last_tweet_id, count=200
            )
        ]
        initial_tweets.extend(new_tweets)
        last_tweet_id = new_tweets[-1].id

    LOGGER.info(f"Found {len(initial_tweets)} tweets for user {twitter_user}")
    return initial_tweets


def get_users_recent_quoted_retweets(
    twitter_user: str, excluded_ids: List[str]
) -> List[Tweet]:
    LOGGER.info(f"Getting tweets for user: {twitter_user}")
    user_tweets = twitter_api.GetUserTimeline(screen_name=twitter_user, count=10)
    return [
        Tweet(t)
        for t in user_tweets
        if t.quoted_status and t.id_str not in excluded_ids
    ]


def find_deleted_tweets(twitter_user: str) -> List[dict]:
    """Get list of tweets that were deleted"""
    bad_ids = []
    list_of_users_to_ignore = ["aaronjmate", "lhfang"]
    tweets = get_all_users_tweets(twitter_user)
    replied_to_statuses = [
        t
        for t in tweets
        if t.replied_to_status_bool
        and t.replied_to_user_screen_name not in list_of_users_to_ignore
    ]
    for t in replied_to_statuses:
        try:
            responded_to_tweet = Tweet(twitter_api.GetStatus(t.replied_to_status_id))
            if responded_to_tweet.quoted_tweet_id:
                quoted_tweet_status = Tweet(
                    twitter_api.GetStatus(responded_to_tweet.quoted_tweet_id)
                )
                LOGGER.info(quoted_tweet_status)
        except TwitterError as e:
            LOGGER.error(f"{e}, {t.replied_to_user_screen_name}, {t.id}")
            bad_ids.append(
                {"user": t.replied_to_user_screen_name, "tweet_id": t.id, "error": e,}
            )

    return bad_ids


def save_status_id_of_replied_to_tweet(tweet: Tweet):
    LOGGER.info(
        msg=f"Adding {tweet.id_str} to {LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME}"
    )
    with open(LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME, "a+") as f:
        f.write(tweet.id_str + "\n")

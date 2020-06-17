from typing import List, Optional

from twitter import Status

from config import TWITTER_API_USER, TWITTER_URL
from _logger import LOGGER


class Tweet:
    """Wrapper class representing a Status (tweet)"""

    def __init__(self, tweet: Status):
        self.raw_tweet: Status = tweet
        self.id: int = self.raw_tweet.id
        self.id_str: str = self.raw_tweet.id_str
        self.text: str = self.raw_tweet.text
        self.user: str = self.raw_tweet.user.screen_name
        self._screen_capture_file_path_quoted_tweet = None

    def __repr__(self) -> str:
        return self.tweet_str

    @property
    def hash_tags(self) -> List[str]:
        return (
            [ht.get("text") for ht in self.raw_tweet.hashtags]
            if self.raw_tweet.hashtags
            else []
        )

    @property
    def quoted_to_status_bool(self) -> bool:
        """Return True if tweet quotes another"""
        # if self.raw_tweet.quoted_status_id:
        #     LOGGER.info(
        #         "At very least this is a retweet, "
        #         "need to confirm if quoting a tweet too"
        #     )
        #     if (
        #             self.raw_tweet.quoted_status_id_str
        #             in [url.expanded_url for url in self.raw_tweet.urls][0]
        #     ):
        #         return True
        # return False
        return False if not self.raw_tweet.quoted_status else True

    @property
    def quoted_status(self) -> Optional[Status]:
        """Return Quoted Status"""
        return self.raw_tweet.quoted_status

    @property
    def quoted_tweet_id(self) -> Optional[str]:
        """Return id of the quoted tweet"""
        return self.raw_tweet.quoted_status_id

    @property
    def quoted_tweet_text(self) -> Optional[str]:
        """Return text of the quoted tweet"""
        if self.quoted_to_status_bool:
            raw_text = self.quoted_status.text
            clean_text = raw_text.replace("&amp;", "&")
            return clean_text.replace(
                f"@{self.quoted_status.in_reply_to_screen_name} ", ""
            )
        return None

    @property
    def quoted_tweet_url(self) -> Optional[str]:
        if self.quoted_status:
            tweet_url = (
                f"{TWITTER_URL}/{self.quoted_tweet_user}/status/{self.quoted_tweet_id}"
            )
            LOGGER.debug(msg=f"Quoted Tweet URL: {tweet_url}")
            return tweet_url
        return None

    @property
    def quoted_tweet_user(self) -> Optional[str]:
        """Returns the user name of the quoted tweet"""
        return self.quoted_status.user.screen_name if self.quoted_status else None

    @property
    def for_the_record_message(self) -> Optional[str]:
        """Message to be tweeted with screen cap of quoted tweet"""
        if self.quoted_to_status_bool:
            message = (
                f'@{self.user} "{self.quoted_tweet_text}" -{self.quoted_tweet_user}'
            )

            LOGGER.debug(msg=message)
            return message

        # return (
        #     f"@{self.user} Cannot include text of quoted tweet because this account "
        #     f"@{TWITTER_API_USER.get('screen_name')} has been blocked by the user of "
        #     f"the quoted tweet."
        # )

    @property
    def replied_to_status_bool(self) -> bool:
        """Return True if tweet replies to another"""
        return False if not self.raw_tweet.in_reply_to_status_id else True

    @property
    def replied_to_status_id(self) -> int:
        """Return True if tweet quotes another"""
        return self.raw_tweet.in_reply_to_status_id

    @property
    def replied_to_tweet_url(self) -> Optional[str]:
        """Return True if tweet quotes another"""
        if self.replied_to_status_bool:
            tweet_url = (
                f"{TWITTER_URL}/{self.replied_to_user_name}/"
                f"status/{self.replied_to_status_id}"
            )
            LOGGER.debug(msg=f"Replied to Tweet URL: {tweet_url}")
            return tweet_url
        return None

    @property
    def replied_to_user_name(self) -> str:
        """Returns screen name of the user that is being replied to"""
        return self.raw_tweet.in_reply_to_screen_name

    @property
    def screen_capture_file_path_quoted_tweet(self) -> Optional[str]:
        return self._screen_capture_file_path_quoted_tweet

    @screen_capture_file_path_quoted_tweet.setter
    def screen_capture_file_path_quoted_tweet(self, value):
        self._screen_capture_file_path_quoted_tweet = value

    @property
    def tweet_str(self) -> str:
        return f"@{self.user}: {self.text}"

    @property
    def tweet_url(self) -> str:
        tweet_url = f"{TWITTER_URL}/{self.user}/status/{self.id}"
        LOGGER.debug(msg=f"Tweet URL: {tweet_url}")
        return tweet_url

    @property
    def urls(self) -> Optional[List[str]]:
        return [url_obj.url for url_obj in self.raw_tweet.urls]

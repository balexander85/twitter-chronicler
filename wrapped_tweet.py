from typing import List, Optional

from twitter import Status

from config import TWITTER_URL
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
        LOGGER.debug(f"Processing Tweet({self.id}) from {self.user}")

    def __repr__(self) -> str:
        return self.tweet_str

    @property
    def tweet_str(self) -> str:
        return f"@{self.user}: {self.text}"

    @property
    def for_the_record_message(self) -> Optional[str]:
        """Message to be tweeted with screen cap of quoted tweet"""
        if self.quoted_status:
            message = (
                f'@{self.user} "{self.quoted_tweet_text}" -.@{self.quoted_tweet_user}'
                # f"This Tweet is available! \n"
                # f"For the blocked and the record!"
            )
            # if self.urls_from_quoted_tweet:
            #     url_string_list = ", ".join(self.urls_from_quoted_tweet)
            #     message += f"\nURL(s) from tweet: {url_string_list}"

            LOGGER.debug(msg=message)
            return message

        return None

    @property
    def quoted_status(self) -> Optional[Status]:
        """Return True if tweet quotes another"""
        return self.raw_tweet.quoted_status

    @property
    def quoted_tweet_id(self) -> Optional[str]:
        """Return id of the quoted tweet"""
        return self.quoted_status.id if self.quoted_status else None

    @property
    def quoted_tweet_locator(self) -> Optional[str]:
        """Return locator for the div of the quoted tweet"""
        return (
            f"div[data-tweet-id='{self.quoted_tweet_id}']"
            if self.quoted_status
            else None
        )

    @property
    def quoted_tweet_text(self) -> Optional[str]:
        """Return locator for the div of the quoted tweet"""
        raw_text = self.quoted_status.text
        # clean_text = " ".join(
        #     [
        #         w
        #         for w in raw_text.split(" ")
        #         if w
        #         not in [f"@{u.screen_name}" for u in self.quoted_status.user_mentions]
        #     ]
        # )
        clean_text = raw_text.replace("&amp;", "&")

        return (
            clean_text.replace(f"@{self.quoted_status.in_reply_to_screen_name} ", "")
            if self.quoted_status
            else None
        )

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
    def screen_capture_file_path_quoted_tweet(self) -> Optional[str]:
        return self._screen_capture_file_path_quoted_tweet

    @screen_capture_file_path_quoted_tweet.setter
    def screen_capture_file_path_quoted_tweet(self, value):
        self._screen_capture_file_path_quoted_tweet = value

    @property
    def tweet_locator(self) -> str:
        return f"div[data-tweet-id='{self.id}']"

    @property
    def urls_from_quoted_tweet(self) -> Optional[List[str]]:
        return (
            [url_obj.url for url_obj in self.quoted_status.urls]
            if self.quoted_status
            else None
        )

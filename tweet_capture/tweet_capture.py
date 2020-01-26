import os
import time
from typing import Optional

from selenium.webdriver.remote.webelement import WebElement

from config import PROJECT_DIR_PATH
from _logger import LOGGER
from wrapped_driver import WrappedWebDriver, scroll_to_element
from wrapped_tweet import Tweet


class TweetCapture:
    """Page object representing div of a tweet"""

    TWEET_DIV_CONTAINER = "div[data-tweet-id='{}']"

    def __init__(self, webdriver: WrappedWebDriver, tweet: Tweet):
        self.driver = webdriver
        self.tweet = tweet
        self.open()

    def _wait_until_loaded(self) -> bool:
        return self.driver.wait_for_element_to_be_visible_by_css(
            locator=self.tweet_locator
        )

    def open(self):
        LOGGER.info(
            f"Opening...tweet quoted by {self.tweet.user} {self.tweet.quoted_tweet_url}"
        )
        self.driver.open(url=self.tweet.quoted_tweet_url)
        time.sleep(5)
        self._wait_until_loaded()

    @property
    def tweet_locator(self) -> str:
        return self.TWEET_DIV_CONTAINER.format(self.tweet.quoted_tweet_id)

    @property
    def tweet_element(self) -> WebElement:
        """WebElement of the Tweet Div"""
        LOGGER.debug(f"Getting tweet_element: {self.tweet_locator}")
        self.driver.wait_for_element_to_be_visible_by_css(locator=self.tweet_locator)
        return self.driver.get_element_by_css(locator=self.tweet_locator)

    @property
    def screen_capture_file_name_quoted_tweet(self) -> Optional[str]:
        return (
            f"tweet_capture_{self.tweet.quoted_tweet_id}.png"
            if self.tweet.quoted_status
            else None
        )

    @property
    def screen_capture_file_path_quoted_tweet(self) -> Optional[str]:
        return (
            os.path.join(
                PROJECT_DIR_PATH,
                "tweet_capture",
                "screen_shots",
                self.screen_capture_file_name_quoted_tweet,
            )
            if self.screen_capture_file_name_quoted_tweet
            else None
        )

    def screen_shot_tweet(self) -> str:
        """Take a screenshot of tweet and save to file"""
        scroll_to_element(driver=self.driver, element=self.tweet_element)
        LOGGER.info(
            msg=f"Saving screen shot: {self.screen_capture_file_path_quoted_tweet}"
        )
        if not self.tweet_element.screenshot(
            filename=self.screen_capture_file_path_quoted_tweet
        ):
            LOGGER.error(f"Failed to save {self.screen_capture_file_path_quoted_tweet}")
            raise Exception(
                f"Failed to save {self.screen_capture_file_path_quoted_tweet}"
            )
        else:
            return self.screen_capture_file_path_quoted_tweet

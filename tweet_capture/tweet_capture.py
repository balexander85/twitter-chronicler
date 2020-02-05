import os

from furl import furl
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from _logger import LOGGER
from wrapped_driver import WrappedWebDriver


MODULE_DIR_PATH = os.path.dirname(__file__)
TWITTER_URL = "https://twitter.com"


class TweetCapture:
    """Page object representing div of a tweet"""

    TWITTER_BODY = "body"

    def __init__(self):
        self.driver = WrappedWebDriver(browser="headless")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.driver.quit_driver()

    def _wait_until_loaded(self) -> bool:
        return self.driver.wait_for_element_to_be_visible_by_css(
            locator=self.TWITTER_BODY
        )

    def open(self, url: str):
        LOGGER.info(f"Opening...tweet: {url}")
        self.driver.open(url=url)
        self._wait_until_loaded()

    def get_tweet_element(self, tweet_locator) -> WebElement:
        """WebElement of the Tweet Div, this assumes tweet page has loaded"""
        LOGGER.debug(f"Retrieving tweet_element")
        try:
            self.driver.wait_for_element_to_be_present_by_css(
                locator=tweet_locator, timeout=10, poll_frequency=1
            )
            return self.driver.get_element_by_css(locator=tweet_locator)
        except TimeoutException as e:
            LOGGER.error(f"{e} timed out looking for: {tweet_locator}")
            self.driver.quit_driver()
            raise TimeoutException

    @staticmethod
    def get_screen_capture_file_path_quoted_tweet(tweet_id) -> str:
        return os.path.join(
            MODULE_DIR_PATH, "screen_shots", f"tweet_capture_{tweet_id}.png",
        )

    def screen_shot_tweet(self, url) -> str:
        """Take a screenshot of tweet and save to file"""
        self.open(url=url)
        tweet_id = furl(url).path.segments[-1]
        tweet_locator = f"div[data-tweet-id='{tweet_id}']"
        self.driver.scroll_to_element(
            element=self.get_tweet_element(tweet_locator=tweet_locator)
        )
        screen_capture_file_path = self.get_screen_capture_file_path_quoted_tweet(
            tweet_id=tweet_id
        )
        LOGGER.info(msg=f"Saving screen shot: {screen_capture_file_path}")
        if not self.get_tweet_element(tweet_locator=tweet_locator).screenshot(
            filename=screen_capture_file_path
        ):
            LOGGER.error(f"Failed to save {screen_capture_file_path}")
            raise Exception(f"Failed to save {screen_capture_file_path}")
        else:
            return screen_capture_file_path

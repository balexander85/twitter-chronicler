import os

from furl import furl
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from _logger import LOGGER
from wrapped_driver import WrappedWebDriver, scroll_to_element


MODULE_DIR_PATH = os.path.dirname(__file__)
TWITTER_URL = "https://twitter.com"


class TweetCapture:
    """Page object representing div of a tweet"""

    LOGIN_BUTTON = "a[data-testid='login']"
    TWEET_DIV_CONTAINER_OLD = "div[data-tweet-id='{}']"
    TWEET_DIV_CONTAINER = "div[data-testid='primaryColumn'] article:nth-of-type(1)"
    TWITTER_BODY = "body"

    def __init__(self, webdriver: WrappedWebDriver, url: str):
        self.driver = webdriver
        self.url = url

    def _wait_until_loaded(self) -> bool:
        return self.driver.wait_for_element_to_be_visible_by_css(
            locator=self.TWITTER_BODY
        )

    def open(self):
        LOGGER.info(f"Opening...tweet: {self.url}")
        self.driver.open(url=self.url)
        self._wait_until_loaded()

    @property
    def tweet_id(self) -> str:
        """From extract out the tweet id from self.url"""
        f_url = furl(self.url)
        return f_url.path.segments[2]

    @property
    def tweet_locator(self) -> str:
        return self.TWEET_DIV_CONTAINER_OLD.format(self.tweet_id)

    @property
    def tweet_element(self) -> WebElement:
        """WebElement of the Tweet Div, this assumes tweet page has loaded"""
        LOGGER.debug(f"Retrieving tweet_element")
        try:
            self.driver.wait_for_element_to_be_present_by_css(
                locator=self.tweet_locator, timeout=10, poll_frequency=1
            )
            return self.driver.get_element_by_css(locator=self.tweet_locator)
        except TimeoutException as e:
            LOGGER.error(f"{e} timed out looking for: {self.tweet_locator}")
            self.driver.quit_driver()
            raise TimeoutException

    @property
    def screen_capture_file_name_quoted_tweet(self) -> str:
        return f"tweet_capture_{self.tweet_id}.png"

    @property
    def screen_capture_file_path_quoted_tweet(self) -> str:
        return os.path.join(
            MODULE_DIR_PATH, "screen_shots", self.screen_capture_file_name_quoted_tweet,
        )

    def screen_shot_tweet(self) -> str:
        """Take a screenshot of tweet and save to file"""
        self.open()
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

import os

from furl import furl
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from config import CHROME_DRIVER_PATH
from _logger import LOGGER
from wrapped_driver import WrappedDriver


MODULE_DIR_PATH = os.path.dirname(__file__)
TWITTER_URL = "https://twitter.com"
TWITTER_USER_AGENT = (
    "user-agent=Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
)


class TweetCapture:
    """Page object representing div of a tweet"""

    TWITTER_BODY = "body"
    TOMBSTONE_VIEW_LINK = "button.Tombstone-action.js-display-this-media.btn-link"

    def __init__(self):
        self.driver = WrappedDriver(
            chrome_driver_path=CHROME_DRIVER_PATH,
            browser="chrome",
            headless=False,
            user_agent=TWITTER_USER_AGENT,
        )

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

    def dismiss_sensitive_material_warning(self):
        """Click View for sensitive material warning"""
        try:
            self.driver.get_element_by_css(self.TOMBSTONE_VIEW_LINK).click()
            self.driver.wait_for_element_not_to_be_visible_by_css(
                self.TOMBSTONE_VIEW_LINK
            )
        except NoSuchElementException as e:
            LOGGER.debug(f"Tombstone warning was not present {e}")
            pass

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
        # move mouse cursor away to highlight any @users
        self.driver.scroll_to_element(
            self.get_tweet_element(tweet_locator=tweet_locator + " span.metadata")
        )
        # Check for translation
        # to be implemented
        # Check for "This media may contain sensitive material."
        self.dismiss_sensitive_material_warning()
        LOGGER.info(msg=f"Saving screen shot: {screen_capture_file_path}")
        if not self.get_tweet_element(tweet_locator=tweet_locator).screenshot(
            filename=screen_capture_file_path
        ):
            LOGGER.error(f"Failed to save {screen_capture_file_path}")
            raise Exception(f"Failed to save {screen_capture_file_path}")
        else:
            return screen_capture_file_path

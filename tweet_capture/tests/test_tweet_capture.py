import pytest

from tweet_capture import TweetCapture
from wrapped_driver import WrappedWebDriver


class TestTweetCapture:
    """
    Verify functionality tweet_capture module
    """

    # @pytest.fixture(autouse=True)
    # def setup(self):
    #     self.driver = WrappedWebDriver(browser="headless")
    #
    # def teardown(self):
    #     self.driver.quit_driver()

    def test_tweet_screen_shot_tweet(self, test_tweet):
        test_tweet = test_tweet("quoted_tweet")
        with TweetCapture() as tweet_capture:
            screen_cap_file_path = tweet_capture.screen_shot_tweet(
                test_tweet.quoted_tweet_url
            )
        # assert tweet_capture.tweet_locator == "div[data-tweet-id='1200946238033661957']"

        assert (
            screen_cap_file_path == "/Users/brian/Development/repos/projects_github/"
            "twitter_chronicler/tweet_capture/screen_shots/"
            "tweet_capture_1200946238033661957.png"
        )

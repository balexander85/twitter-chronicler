from typing import List

from retry import retry
from selenium.common.exceptions import TimeoutException

from _logger import LOGGER
from tweet_capture import TweetCapture
from twitter_helpers import post_collected_tweets
from wrapped_driver import WrappedWebDriver
from wrapped_tweet import Tweet


def collect_and_post_tweets(tweets):

    if tweets:
        collect_quoted_tweets(quoted_tweets=tweets)
        post_collected_tweets(tweets)


@retry(exceptions=TimeoutException, tries=4, delay=2)
def collect_quoted_tweets(quoted_tweets: List[Tweet]):
    """Loop through list of quoted tweets and screen cap them"""
    with WrappedWebDriver(browser="headless") as driver:
        for tweet in quoted_tweets:
            screen_shot_file_path = TweetCapture(
                webdriver=driver, tweet=tweet
            ).screen_shot_tweet()
            add_screen_shot_to_tweet(
                tweet=tweet, screen_shot_file_path=screen_shot_file_path
            )


def add_screen_shot_to_tweet(tweet: Tweet, screen_shot_file_path: str):
    """Add the path of the screenshot to the tweet instance"""
    LOGGER.info(f"Adding {screen_shot_file_path} to the tweet instance {tweet.id_str}")
    tweet.screen_capture_file_path_quoted_tweet = screen_shot_file_path


class Chronicler:
    """
    Potential class for methods dealing with more than an individual tweet
    but more of the collecting and posting screen captures

    maybe include:
        * for_the_record_message property
        * post_reply_to_user_tweet
    """

    ...

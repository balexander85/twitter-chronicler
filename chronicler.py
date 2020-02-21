"""chronicler.py

Containing some helpful objects

1. List of users to follow
2. for each user watch for retweets that quote tweets
3. save screenshot of quoted tweet
4. save URL(s) from quoted tweet
5. Reply to tweet with image of quoted tweet with URL(s) and a disclaimer

This Tweet is available!

Note:
    I was tired of looking at tweets that quoted tweets
    where the quoted tweets had been deleted.
"""
from typing import List

from retry import retry
from selenium.common.exceptions import TimeoutException

from config import LIST_OF_USERS_TO_FOLLOW
from _logger import LOGGER
from tweet_capture import TweetCapture
from twitter_helpers import (
    find_quoted_tweets,
    get_tweet_from_url,
    post_collected_tweets,
)
from wrapped_tweet import Tweet


def run_chronicler():
    LOGGER.info("Start of script")

    for user in LIST_OF_USERS_TO_FOLLOW:
        user_quoted_retweets = find_quoted_tweets(users_to_follow=user)
        collect_and_post_tweets(user_quoted_retweets)

    LOGGER.info("End of script run")


def run_chronicler_ad_hoc():
    LOGGER.info("Starting Ad-hoc script")
    user_quoted_retweets_urls: List[str] = []
    user_quoted_retweets: List[Tweet] = [
        get_tweet_from_url(url) for url in user_quoted_retweets_urls
    ]
    collect_and_post_tweets(user_quoted_retweets)

    LOGGER.info("End of Ad-hoc script run")


def collect_and_post_tweets(tweets: List[Tweet]):

    if tweets:
        collect_quoted_tweets(quoted_tweets=tweets)
        post_collected_tweets(tweets)


@retry(exceptions=TimeoutException, tries=4, delay=2)
def collect_quoted_tweets(quoted_tweets: List[Tweet]):
    """Loop through list of quoted tweets and screen cap them"""
    with TweetCapture() as tweet_capture:
        for tweet in quoted_tweets:
            screen_shot_file_path = tweet_capture.screen_shot_tweet(
                url=tweet.quoted_tweet_url
            )
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

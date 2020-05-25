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
from pathlib import Path
from typing import List

from config import LIST_OF_USERS_TO_FOLLOW
from _logger import LOGGER
from tweet_capture import TweetCapture
from twitter_helpers import (
    add_screenshot_to_tweet,
    find_quoted_tweets,
    get_tweet_from_url,
    post_collected_tweets,
)
from wrapped_tweet import Tweet


def run_chronicler():
    LOGGER.info("Start of script")

    for user in LIST_OF_USERS_TO_FOLLOW:
        LOGGER.info(f"starting collection for user: @{user}")
        user_quoted_retweets = find_quoted_tweets(user=user)
        collect_and_post_tweets(user_quoted_retweets)
        LOGGER.info(f"ending collection for user: @{user}")

    LOGGER.info("End of script run")


def run_chronicler_ad_hoc():
    """Helper function to run chronicler for list of urls for possible redo's

    Example of user_quoted_retweets_urls list:

        ['https://twitter.com/_b_axe/status/1236662806163984385', '...']

    """
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


def collect_quoted_tweets(quoted_tweets: List[Tweet]):
    """Loop through list of quoted tweets and screen cap them"""
    screenshot_dir = Path(__file__).parent
    with TweetCapture(screenshot_dir=screenshot_dir) as tweet_capture:
        for tweet in quoted_tweets:
            screenshot_file_path = tweet_capture.screen_capture_tweet(
                url=tweet.quoted_tweet_url
            )
            add_screenshot_to_tweet(
                tweet=tweet, screen_shot_file_path=screenshot_file_path
            )


class Chronicler:
    """
    Potential class for methods dealing with more than an individual tweet
    but more of the collecting and posting screen captures

    maybe include:
        * for_the_record_message property
        * post_reply_to_user_tweet
    """

    ...


if __name__ == "__main__":
    run_chronicler_ad_hoc()

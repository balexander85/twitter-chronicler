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

from config import CHROME_DRIVER_PATH, LIST_OF_USERS_TO_FOLLOW
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
    with TweetCapture(
        chrome_driver_path=CHROME_DRIVER_PATH,
        screenshot_dir=screenshot_dir,
        headless=True,
    ) as tweet_capture:
        for tweet in quoted_tweets:
            screenshot_file_path = tweet_capture.screen_capture_tweet(
                url=tweet.quoted_tweet_url
            )
            add_screenshot_to_tweet(
                tweet=tweet, screen_shot_file_path=screenshot_file_path
            )


class Chronicler:
    """
    Scan user's recent tweets (10) for retweets that quote a tweet. For
    each tweet that is quoted by user (exceptions apply), screen capture
    the quoted tweet and reply to user with a screenshot of quoted tweet.

    Exceptions:
        * Retweet has already been replied to
        * Retweet that quotes the user's own tweet
        * Retweet that quotes a tweet that is created by bot user
        * Retweet that quotes the same tweet that was quoted in same thread

    Notes:
        * I created this because I was tired of looking at tweets that
          quoted tweets where the quoted tweets had been deleted.

        * The quoted tweet with the screenshot should include as much text
          from the tweet as possible so that users that have screen readers
          can have some clue as to the text of the quoted tweet.

        * If a user starts a thread by quoting a tweet and then later in
          the thread the user quotes a different tweet both tweets should
          be collected.

        * If user blocks the bot or their account is private or suspended
          then skip collection

    To be implemented:
        * Handle error if user blocks bot or their account is private or suspended
        * Collect tweet if user quotes tweet where the user of the quoted tweet
          blocks the bot
        * Send notification if user blocks bot or their account is private or suspended
        * Add ability for user to request a tweet be screen capped
        * Add ability for user to request screenshot of a tweet that is quoted by user
          where the user of the quoted tweet blocked the requesting user
        * Keep track of number of twitter api calls made

    """

    ...


if __name__ == "__main__":
    run_chronicler_ad_hoc()

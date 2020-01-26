"""chronicle_tweets.py

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

from _logger import LOGGER
from chronicler import collect_and_post_tweets
from config import LIST_OF_USERS_TO_FOLLOW
from twitter_helpers import find_quoted_tweets


def run_chronicler():
    LOGGER.info("Start of script")

    user_quoted_retweets = find_quoted_tweets(users_to_follow=LIST_OF_USERS_TO_FOLLOW)
    collect_and_post_tweets(user_quoted_retweets)

    LOGGER.info("End of script run")


if __name__ == "__main__":
    run_chronicler()

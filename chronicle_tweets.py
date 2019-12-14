"""chronicle_tweets.py

Containing some helpful objects

1. List of users to follow
2. for each user watch for retweets that quote tweets
3. save screenshot of quoted tweet
4. save URL(s) from quoted tweet
5. Reply to tweet with image of quoted tweet with URL(s) and a disclaimer

This Tweet is available!

I was tired of looking at retweets that quoted tweets that had been deleted.
"""
import time
from typing import List

from config import LIST_OF_USERS_TO_FOLLOW, LIST_OF_STATUS_IDS_REPLIED_TO
from wrapped_driver import WrappedWebDriver, screen_capture_element, scroll_to_element
from util import LOGGER, twitter_api, Tweet, save_status_id_of_replied_to_tweet


def collect_quoted_tweets(quoted_tweets: List[Tweet]):
    """Loop through list of quoted tweets and screen cap them"""
    driver = WrappedWebDriver(browser="headless")
    for tweet in quoted_tweets:
        driver.open(url=tweet.quoted_tweet_url)
        tweet_locator = tweet.quoted_tweet_locator
        tweet_element = driver.get_element_by_css(locator=tweet_locator)
        scroll_to_element(driver=driver, element=tweet_element)
        time.sleep(1)
        screen_capture_element(
            element=tweet_element, file_name=tweet.screen_capture_file_name_quoted_tweet
        )
    driver.quit_driver()


def post_collected_tweets(quoted_tweets: List[Tweet]):
    """Post"""
    for user_tweet in quoted_tweets:
        LOGGER.info(msg=user_tweet)
        status_message = get_status_message(
            retweet_user=user_tweet.user,
            urls_in_quoted_tweet=user_tweet.urls_from_quoted_tweet,
        )
        response = twitter_api.PostUpdate(
            status=status_message,
            media=f"screen_shots/{user_tweet.screen_capture_file_name_quoted_tweet}",
            in_reply_to_status_id=user_tweet.id,
        )
        LOGGER.info(response)
        save_status_id_of_replied_to_tweet(tweet=user_tweet)


def get_status_message(retweet_user: str, urls_in_quoted_tweet: List[str]) -> str:
    if urls_in_quoted_tweet:
        url_string_list = ", ".join(urls_in_quoted_tweet)
        message = (
            f"@{retweet_user} This Tweet is available! \n"
            f"For the blocked and the record!\n"
            f"URL(s) from tweet: {url_string_list}"
        )
    else:
        message = (
            f"@{retweet_user} This Tweet is available! \n"
            f"For the blocked and the record!"
        )
    LOGGER.info(msg=message)
    return message


if __name__ == "__main__":

    for twitter_user in LIST_OF_USERS_TO_FOLLOW:
        user_tweets = twitter_api.GetUserTimeline(screen_name=twitter_user, count=10)
        user_quoted_retweets: List[Tweet] = [
            Tweet(t)
            for t in user_tweets
            if t.quoted_status and t.id_str not in LIST_OF_STATUS_IDS_REPLIED_TO
        ]
        if user_quoted_retweets:
            collect_quoted_tweets(user_quoted_retweets)
            post_collected_tweets(user_quoted_retweets)
        else:
            LOGGER.info(msg=f"No new retweets for user: {twitter_user}")

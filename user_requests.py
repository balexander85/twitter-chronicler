"""user_requests.py

Take screenshot of quoted tweet upon user request
"""
from collections import defaultdict
from pathlib import Path
from typing import List

from twitter import Status

from config import (
    CHROME_DRIVER_PATH,
    LIST_OF_REQUESTS_IDS_COMPLETED,
    LIST_OF_REQUESTS_IDS_COMPLETED_FILE_NAME,
)
from _logger import LOGGER
from tweet_capture import TweetCapture
from twitter_helpers import (
    add_screenshot_to_tweet,
    get_status,
    twitter_api,
)
from util import add_status_id_to_file
from wrapped_tweet import Tweet


def collect_requests_and_post_tweets():
    """Get list of statuses from requests and post replies"""
    latest_id = (
        LIST_OF_REQUESTS_IDS_COMPLETED[-1] if LIST_OF_REQUESTS_IDS_COMPLETED else None
    )
    requests = search_for_requests(since_id=latest_id)
    if requests:
        for request_type, tweets in requests.items():
            if request_type == "screenshot":
                process_screenshot_requests(items=tweets)
            elif request_type == "ftb":
                process_for_the_blocked_requests(items=tweets)


def process_screenshot_requests(items):
    """Process requests for screenshots"""
    screenshot_dir = Path(__file__).parent
    with TweetCapture(
        chrome_driver_path=CHROME_DRIVER_PATH,
        screenshot_dir=screenshot_dir,
        headless=True,
    ) as tweet_capture:
        for item in items:
            replied_to_tweet = Tweet(get_status(status_id=item.replied_to_status_id))
            screen_shot_file_path = tweet_capture.screen_shot_tweet(
                url=replied_to_tweet.tweet_url
            )
            add_screenshot_to_tweet(
                tweet=replied_to_tweet, screen_shot_file_path=screen_shot_file_path
            )
            LOGGER.info(msg=f"Replying to '@{item.user}: tweet({item.id})'")
            status_message = (
                f'@{item.user} "{replied_to_tweet.text}" '
                f"-{item.replied_to_user_name}"
            )
            response: Status = twitter_api.PostUpdate(
                status=status_message,
                media=replied_to_tweet.screen_capture_file_path_quoted_tweet,
                in_reply_to_status_id=item.id,
            )
            LOGGER.debug(
                f"request.id: {item.id} "
                f"response.id: {response.id} "
                f"in_reply_to_status_id: {response.in_reply_to_status_id} "
                f"in_reply_to_screen_name: {response.in_reply_to_screen_name}"
            )
            tweet_reply_id = response.in_reply_to_status_id
            if not tweet_reply_id:
                raise Exception(f"The tweet_reply_id was None.")
            add_status_id_to_file(
                tweet_id=str(tweet_reply_id),
                list_of_ids_replied_to_file_name=LIST_OF_REQUESTS_IDS_COMPLETED_FILE_NAME,
            )


def process_for_the_blocked_requests(items):
    """Process requests for users needing screenshot because they're blocked"""
    ...


def search_for_requests(since_id: str = None) -> defaultdict:
    """Function to find requests from users that want tweet screen captured

    Notes:
        * Search recent mentions for tweets requesting screenshot
        * Return Status IDs for Statuses that have one of the acceptable phrases
    """
    tweets = defaultdict(list)
    mentions: List[Status] = twitter_api.GetMentions(since_id=since_id)
    for mention in mentions:
        tweet = Tweet(mention)
        # Verify the mention is in reply to a tweet
        if tweet.replied_to_status_bool:
            if "screenshot" in tweet.hash_tags:
                # Take screenshot of the tweet replied to
                LOGGER.info(f"Text {tweet.id} matches {tweet}")
                tweets["screenshot"].append(tweet)
            elif "ftb" in tweet.hash_tags:
                # Take screenshot of the tweet quoted by tweet replied to
                LOGGER.info(f"Text {tweet.id} matches {tweet}")
                tweets["ftb"].append(tweet)
            else:
                LOGGER.debug(
                    f"Mention id({mention}) did not contain one of the expected text"
                )

    LOGGER.info(f"Returning tweets: {tweets}")
    return tweets


if __name__ == "__main__":
    collect_requests_and_post_tweets()

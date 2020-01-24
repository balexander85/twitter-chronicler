import os
from typing import List, Optional, Union

from retrying import retry
from twitter import Api as twitterApi
from twitter import Status, TwitterError
from selenium.common.exceptions import TimeoutException
from wrapped_driver import WrappedWebDriver, scroll_to_element

from config import (
    APP_KEY,
    APP_SECRET,
    LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME,
    LIST_OF_STATUS_IDS_REPLIED_TO,
    PROJECT_DIR_PATH,
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET,
    TWITTER_API_USER,
    TWITTER_URL,
)
from _logger import LOGGER


twitter_api = twitterApi(
    consumer_key=APP_KEY,
    consumer_secret=APP_SECRET,
    access_token_key=OAUTH_TOKEN,
    access_token_secret=OAUTH_TOKEN_SECRET,
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


class Tweet:
    """Wrapper class representing a Status (tweet)"""

    def __init__(self, tweet: Status):
        self.raw_tweet: Status = tweet
        self.id: int = self.raw_tweet.id
        self.id_str: str = self.raw_tweet.id_str
        self.text: str = self.raw_tweet.text
        self.user: str = self.raw_tweet.user.screen_name

    def __repr__(self):
        tweet = f"@{self.user}: {self.text}"
        LOGGER.debug(f"Processing '{tweet}'")
        return tweet

    @property
    def for_the_record_message(self) -> Optional[str]:
        """Message to be tweeted with screen cap of quoted tweet"""
        if self.quoted_status:
            message = (
                f"@{self.user} "
                f"This Tweet is available! \n"
                f"For the blocked and the record!"
            )
            if self.urls_from_quoted_tweet:
                url_string_list = ", ".join(self.urls_from_quoted_tweet)
                message += f"\nURL(s) from tweet: {url_string_list}"

            LOGGER.debug(msg=message)
            return message

        return None

    @property
    def quoted_status(self) -> Optional[Status]:
        """Return True if tweet quotes another"""
        return self.raw_tweet.quoted_status

    @property
    def quoted_tweet_id(self) -> Optional[str]:
        """Return id of the quoted tweet"""
        return self.quoted_status.id if self.quoted_status else None

    @property
    def quoted_tweet_locator(self) -> Optional[str]:
        """Return locator for the div of the quoted tweet"""
        return (
            f"div[data-tweet-id='{self.quoted_tweet_id}']"
            if self.quoted_status
            else None
        )

    @property
    def quoted_tweet_url(self) -> Optional[str]:
        if self.quoted_status:
            tweet_url = (
                f"{TWITTER_URL}/{self.quoted_tweet_user}/status/{self.quoted_tweet_id}"
            )
            LOGGER.debug(msg=f"Quoted Tweet URL: {tweet_url}")
            return tweet_url
        return None

    @property
    def quoted_tweet_user(self) -> Optional[str]:
        """Returns the user name of the quoted tweet"""
        return self.quoted_status.user.screen_name if self.quoted_status else None

    @property
    def replied_to_status_bool(self) -> bool:
        """Return True if tweet quotes another"""
        return False if not self.raw_tweet.in_reply_to_status_id else True

    @property
    def replied_to_status_id(self) -> int:
        """Return True if tweet quotes another"""
        return self.raw_tweet.in_reply_to_status_id

    @property
    def replied_to_user_screen_name(self) -> str:
        """Returns screen name of the user that is being replied to"""
        return self.raw_tweet.in_reply_to_screen_name

    @property
    def screen_capture_file_name_quoted_tweet(self) -> Optional[str]:
        return (
            f"tweet_capture_{self.quoted_tweet_id}.png" if self.quoted_status else None
        )

    @property
    def screen_capture_file_path_quoted_tweet(self) -> Optional[str]:
        return (
            os.path.join(
                PROJECT_DIR_PATH,
                "screen_shots",
                self.screen_capture_file_name_quoted_tweet,
            )
            if self.screen_capture_file_name_quoted_tweet
            else None
        )

    @property
    def tweet_locator(self) -> str:
        return f"div[data-tweet-id='{self.id}']"

    @property
    def urls_from_quoted_tweet(self) -> Optional[List[str]]:
        return (
            [url_obj.url for url_obj in self.quoted_status.urls]
            if self.quoted_status
            else None
        )


def collect_and_post_tweets(tweets):

    if tweets:
        collect_quoted_tweets(quoted_tweets=tweets)
        post_collected_tweets(tweets)


def collect_quoted_tweets(quoted_tweets: List[Tweet]):
    """Loop through list of quoted tweets and screen cap them"""
    driver = WrappedWebDriver(browser="headless")
    for tweet in quoted_tweets:
        collect_tweet(driver=driver, tweet=tweet)
    driver.quit_driver()


@retry(wait_fixed=60, stop_max_attempt_number=5, retry_on_exception=True)
def collect_tweet(driver: WrappedWebDriver, tweet: Tweet):
    """Using webdriver screen capture tweet"""
    LOGGER.info(f"Opening...tweet quoted by {tweet.user} {tweet.quoted_tweet_url}")
    driver.open(url=tweet.quoted_tweet_url)
    LOGGER.debug(f"Getting locator: {tweet.quoted_tweet_locator}")
    quoted_tweet_element = driver.get_element_by_css(locator=tweet.quoted_tweet_locator)
    scroll_to_element(driver=driver, element=quoted_tweet_element)
    LOGGER.info(
        msg=f"Saving screen shot: {tweet.screen_capture_file_path_quoted_tweet}"
    )
    if not quoted_tweet_element.screenshot(
        filename=tweet.screen_capture_file_path_quoted_tweet
    ):
        LOGGER.error(f"Failed to save {tweet.screen_capture_file_path_quoted_tweet}")
        raise Exception(f"Failed to save {tweet.screen_capture_file_path_quoted_tweet}")


def find_quoted_tweets(users_to_follow: List[str]) -> List[Tweet]:
    return [
        tweets
        for user in users_to_follow
        for tweets in get_recent_quoted_retweets_for_user(
            twitter_user=user, excluded_ids=LIST_OF_STATUS_IDS_REPLIED_TO
        )
    ]


def get_status(status_id: Union[int, str]) -> Status:
    """Get tweet from api and return Tweet object"""
    LOGGER.info(f"Fetching tweet with id {status_id}")
    response = twitter_api.GetStatus(status_id=status_id)
    return response


def get_tweet(tweet_id: Union[int, str]) -> Tweet:
    """Get tweet from api and return Tweet object"""
    LOGGER.info(f"Fetching tweet with id {tweet_id}")
    response = get_status(status_id=tweet_id)
    return Tweet(response)


def get_all_users_tweets(twitter_user: str) -> List[Tweet]:
    """Helper method to collect ALL of a user's tweets"""
    LOGGER.info(f"Getting tweets for user: {twitter_user}")
    initial_tweets = [
        Tweet(t)
        for t in twitter_api.GetUserTimeline(screen_name=twitter_user, count=200)
    ]
    last_tweet_id = initial_tweets[-1].id
    user_tweet_count = twitter_api.GetUser(screen_name=twitter_user).statuses_count
    if int(user_tweet_count) > 1000:
        raise Exception("Whatever the hourly rate limit would be raise error for now")

    for _ in range(int(user_tweet_count / 200)):
        new_tweets = [
            Tweet(t)
            for t in twitter_api.GetUserTimeline(
                screen_name=twitter_user, max_id=last_tweet_id, count=200
            )
        ]
        initial_tweets.extend(new_tweets)
        last_tweet_id = new_tweets[-1].id

    LOGGER.info(f"Found {len(initial_tweets)} tweets for user {twitter_user}")
    return initial_tweets


def get_recent_tweets_for_user(twitter_user: str, count: int = 10) -> List[Status]:
    """Using Twitter API get recent tweets using user screen name"""
    LOGGER.debug(f"Getting last {count} tweets for user: {twitter_user}")
    return twitter_api.GetUserTimeline(
        screen_name=twitter_user, since_id=None, count=count
    )


def get_recent_quoted_retweets_for_user(
    twitter_user: str, excluded_ids: List[str]
) -> List[Tweet]:
    """Get tweets for given user that has recently quoted tweet in retweet"""
    user_tweets: List[Status] = get_recent_tweets_for_user(twitter_user=twitter_user)
    user_tweets_quoting_tweets = []
    for t in user_tweets:
        if t.quoted_status:
            tweet = Tweet(t)
            if tweet.quoted_tweet_user == TWITTER_API_USER.get("screen_name"):
                LOGGER.debug(
                    f"Skipping tweet({tweet.quoted_tweet_id}) "
                    f"from @{tweet.user}'s tweet({tweet.id}) quotes the bot user"
                )
            elif tweet.id_str in excluded_ids:
                LOGGER.debug(
                    f"Skipping tweet({tweet.quoted_tweet_id}) from @{tweet.user}'s "
                    f"tweet({tweet.id}) because tweet is in excluded_ids list"
                )
            else:
                LOGGER.debug(
                    f"Adding tweet({tweet.quoted_tweet_id}) from "
                    f"@{tweet.user}'s tweet({tweet.id}) to list of tweets to collect"
                )
                user_tweets_quoting_tweets.append(tweet)
        else:
            LOGGER.debug(
                f"Skipping tweet({t.id}) from @{t.user.screen_name} non-retweet"
            )

    if not user_tweets_quoting_tweets:
        LOGGER.debug(msg=f"No recent retweets for user: {twitter_user}")

    return user_tweets_quoting_tweets


def find_deleted_tweets(twitter_user: str) -> List[dict]:
    """Get list of tweets that were deleted"""
    bad_ids = []
    list_of_users_to_ignore = ["aaronjmate", "lhfang"]
    tweets = get_all_users_tweets(twitter_user)
    replied_to_statuses = [
        t
        for t in tweets
        if t.replied_to_status_bool
        and t.replied_to_user_screen_name not in list_of_users_to_ignore
    ]
    for t in replied_to_statuses:
        try:
            responded_to_tweet = Tweet(twitter_api.GetStatus(t.replied_to_status_id))
            if responded_to_tweet.quoted_tweet_id:
                quoted_tweet_status = Tweet(
                    twitter_api.GetStatus(responded_to_tweet.quoted_tweet_id)
                )
                LOGGER.info(quoted_tweet_status)
        except TwitterError as e:
            LOGGER.error(f"{e}, {t.replied_to_user_screen_name}, {t.id}")
            bad_ids.append(
                {"user": t.replied_to_user_screen_name, "tweet_id": t.id, "error": e,}
            )

    return bad_ids


def save_status_id_of_replied_to_tweet(tweet_id: str):
    """Save id of the replied to tweet

    Save id to file so that tweet will not be replied to more than once.
    """
    LOGGER.debug(msg=f"Adding {tweet_id} to {LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME}")
    with open(LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME, "a+") as f:
        f.write(tweet_id + "\n")


def post_collected_tweets(quoted_tweets: List[Tweet]):
    """For each quoted tweet post for the record and for the blocked"""
    for user_tweet in quoted_tweets:
        response = post_reply_to_user_tweet(tweet=user_tweet)
        save_status_id_of_replied_to_tweet(tweet_id=str(response.in_reply_to_status_id))


def post_reply_to_user_tweet(tweet: Tweet) -> Status:
    """Post message and screen cap of the quoted tweet"""
    LOGGER.info(msg=f"Replying to '@{tweet.user}: tweet({tweet.id})'")
    response: Status = twitter_api.PostUpdate(
        status=tweet.for_the_record_message,
        media=tweet.screen_capture_file_path_quoted_tweet,
        in_reply_to_status_id=tweet.id,
    )
    LOGGER.debug(
        f"tweet.id: {tweet.id} "
        f"response.id: {response.id} "
        f"in_reply_to_status_id: {response.in_reply_to_status_id} "
        f"in_reply_to_screen_name: {response.in_reply_to_screen_name}"
    )
    return response

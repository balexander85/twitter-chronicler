from time import sleep
from typing import List, Union, Optional

from retry import retry
from twitter import Api, Status, TwitterError

from config import (
    CHECKED_STATUSES_DIR_PATH,
    LIST_OF_STATUS_IDS_REPLIED_TO_FILE,
    LIST_OF_STATUS_IDS_REPLIED_TO,
    TWITTER_API_USER,
    READ_APP_KEY,
    READ_APP_SECRET,
    READ_OAUTH_TOKEN,
    READ_OAUTH_TOKEN_SECRET,
    WRITE_APP_KEY,
    WRITE_APP_SECRET,
    WRITE_OAUTH_TOKEN,
    WRITE_OAUTH_TOKEN_SECRET,
)
from _logger import get_module_logger
from wrapped_tweet import Tweet
from util import add_line_to_file


LOGGER = get_module_logger(__name__)

tweet_scanner_api = Api(
    consumer_key=READ_APP_KEY,
    consumer_secret=READ_APP_SECRET,
    access_token_key=READ_OAUTH_TOKEN,
    access_token_secret=READ_OAUTH_TOKEN_SECRET,
    sleep_on_rate_limit=True,
)

tweeter_api = Api(
    consumer_key=WRITE_APP_KEY,
    consumer_secret=WRITE_APP_SECRET,
    access_token_key=WRITE_OAUTH_TOKEN,
    access_token_secret=WRITE_OAUTH_TOKEN_SECRET,
    sleep_on_rate_limit=True,
)


class TwitterRateLimitException(TwitterError):
    pass


def add_screenshot_to_tweet(tweet: Tweet, screen_shot_file_path: str):
    """Add the path of the screenshot to the tweet instance"""
    LOGGER.debug(f"Adding {screen_shot_file_path} to the tweet instance {tweet.id_str}")
    tweet.screen_capture_file_path_quoted_tweet = screen_shot_file_path


def check_for_last_status_id(file_name: str) -> int:
    """Look for user file and get last status id checked"""
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
            latest_status_ids: List = list(
                filter(None, map(lambda line: line.strip("\n"), lines))
            )
            latest_status_id = (
                int(latest_status_ids[-1]) if len(latest_status_ids) > 0 else None
            )
            LOGGER.debug(f"Last status id checked {latest_status_id}")
            return latest_status_id
    except FileNotFoundError:
        LOGGER.info(f"No status id file has been created {file_name}")


def get_status(api_user, status_id: Union[int, str]) -> Status:
    """Get tweet from api and return Tweet object"""
    LOGGER.info(f"api_user.GetStatus(status_id={status_id})")
    response = api_user.GetStatus(status_id=status_id)
    return response


@retry(exceptions=TwitterRateLimitException, tries=4, delay=2)
def get_recent_tweets_for_user(
    twitter_user: str, since_id: int = None, count: int = 10
) -> List[Status]:
    """Using Twitter API get recent tweets using user screen name"""
    try:
        LOGGER.debug(f"Getting last {count} tweets for user: {twitter_user}")
        response = tweet_scanner_api.GetUserTimeline(
            screen_name=twitter_user, since_id=since_id, count=count
        )
        return response
    except TwitterError as errors:
        if type(errors) == list:
            for error in errors.message:
                error_code = error.get("code")
                if error_code == 88:
                    LOGGER.error(
                        f"'Rate limit exceeded': "
                        f"unable to retrieve recent tweets for {twitter_user}. {error}"
                    )
                    sleep_time = 120
                    LOGGER.error(f"Sleeping for {sleep_time} seconds")
                    sleep(sleep_time)
                    raise TwitterRateLimitException
                elif error_code == 136:
                    LOGGER.error(
                        f"You have been blocked from viewing "
                        f"this user's ({twitter_user}) profile. {error}"
                    )
                elif error_code == 326:
                    LOGGER.critical(
                        f"'This account is temporarily locked, please login': "
                        f"unable to retrieve recent tweets for {twitter_user}. {error}"
                    )
                else:
                    LOGGER.error(
                        f"Something happened, unable to retrieve recent "
                        f"tweets for {twitter_user}. {error}"
                    )
        else:
            LOGGER.error(
                f"Something happened, unable to retrieve recent "
                f"tweets for {twitter_user}. {errors}"
            )


def find_quoted_tweets(user: str) -> List[Tweet]:
    """Get list of tweets that were quoted by users from given list

    For each user in list of users get user's recent tweets that
    were quoting other tweets. Exclude tweet ids that have already
    been replied to from a previous run.

    Args:
        user: twitter handle w/out @ symbol

    Returns:
        A list of Tweet objects
    """
    user_status_file_path = str(CHECKED_STATUSES_DIR_PATH.joinpath(f"{user}.txt"))
    last_status_id = check_for_last_status_id(file_name=user_status_file_path)
    user_tweets: List[Status] = get_recent_tweets_for_user(
        twitter_user=user, since_id=last_status_id
    )
    if user_tweets:
        LOGGER.debug(
            f"Found {len(user_tweets)} "
            f"{'tweets' if len(user_tweets) > 1 else 'tweet'} for {user}"
        )
        add_line_to_file(line=user_tweets[0].id_str, file_path=user_status_file_path)
    else:
        LOGGER.debug(f"No new tweets from {user} since {last_status_id}")
        return []

    user_tweets_quoting_tweets = list(
        filter(
            None,
            map(
                lambda tweet: process_tweet(
                    status=tweet, excluded_ids=LIST_OF_STATUS_IDS_REPLIED_TO
                ),
                user_tweets,
            ),
        )
    )

    if not user_tweets_quoting_tweets:
        LOGGER.debug(msg=f"No new retweets for user: @{user}")
        return []

    LOGGER.info(
        f"Collecting quoted {'tweets' if len(user_tweets) > 1 else 'tweet'} "
        f"for user: @{user}"
    )

    return user_tweets_quoting_tweets


def post_collected_tweets(quoted_tweets: List[Tweet]) -> bool:
    """For each quoted tweet post for the record and for the blocked"""
    for user_tweet in quoted_tweets:
        response = post_reply_to_user_tweet(tweet=user_tweet)
        tweet_reply_id = response.in_reply_to_status_id
        if not tweet_reply_id:
            LOGGER.info(f"The tweet_reply_id was None.")
        else:
            add_line_to_file(
                line=str(tweet_reply_id),
                file_path=str(LIST_OF_STATUS_IDS_REPLIED_TO_FILE),
            )
    return True


def post_reply_to_user_tweet(tweet: Tweet) -> Status:
    """Post message and screen cap of the quoted tweet"""
    LOGGER.info(msg=f"Replying to '@{tweet.user}: tweet({tweet.id})'")
    response: Status = tweeter_api.PostUpdate(
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


def process_tweet(status: Status, excluded_ids: List[str] = None) -> Optional[Tweet]:
    """Determine if the Status should be documented

    Notes:
        * Skip if tweet does not quote tweet
        * Skip if the quoted_tweet_user is the twitter api account
        * Skip if the user quotes their own tweet
        * Skip if the tweet.id is in excluded list (b/c already been replied to)
        * Skip if the tweet has already been quoted in same thread
    """
    excluded_ids = excluded_ids if excluded_ids else []
    tweet = Tweet(status)
    if tweet.quoted_to_status_bool:
        quoted_tweet_user = tweet.quoted_tweet_user
        if quoted_tweet_user == TWITTER_API_USER.get("screen_name"):
            LOGGER.debug(
                f"Skipping: Tweet({tweet.id}) from @{tweet.user} quotes bot user tweet"
            )
        elif quoted_tweet_user == tweet.user:
            LOGGER.debug(
                f"Skipping: Tweet({tweet.id}) from @{tweet.user} quotes their own tweet"
            )
        elif tweet.id_str in excluded_ids:
            LOGGER.debug(
                f"Skipping: Tweet({tweet.id}) from @{tweet.user} "
                f"because tweet has been replied to."
            )
        elif (
            tweet.replied_to_status_bool
            and str(tweet.replied_to_status_id) in excluded_ids
        ):
            LOGGER.info(
                f"@{tweet.user}'s Tweet({tweet.id}) quotes "
                f"Tweet({tweet.quoted_tweet_id}) but replied to a "
                f"Tweet({tweet.replied_to_status_id}) that has already "
                f"been processed. Get response for the replied_to_status "
                f"to verify if the two tweets are quoting same tweet."
            )
            replied_to_tweet = Tweet(
                get_status(tweet_scanner_api, tweet.replied_to_status_id)
            )
            if replied_to_tweet.quoted_tweet_id == tweet.quoted_tweet_id:
                LOGGER.info(
                    f"Skipping: Tweet({tweet.id}) from @{tweet.user} quoted "
                    f"Tweet({tweet.quoted_tweet_id}) was already quoted by "
                    f"user in same thread"
                )
            else:
                LOGGER.info(
                    f"The Tweet({tweet.id}) is quoting a different tweet than "
                    f"the Tweet({tweet.replied_to_status_id}) that was replied to. "
                    f"Adding Tweet({tweet.quoted_tweet_id}) from @{tweet.user}'s"
                    f"tweet({tweet.id}) to list of tweets to collect"
                )
                return tweet
        else:
            LOGGER.debug(
                f"Adding Tweet({tweet.quoted_tweet_id}) from @{tweet.user}'s "
                f"Tweet({tweet.id}) to list of tweets to collect"
            )
            return tweet
    else:
        LOGGER.debug(
            f"Skipping: Tweet({status.id}) from @{status.user.screen_name} non-retweet"
        )


if __name__ == "__main__":
    LOGGER.info("End of file")

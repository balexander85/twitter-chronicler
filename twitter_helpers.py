import json
from pathlib import Path
from time import sleep
from typing import List, Union, Optional

from furl import furl
from twitter import Api, Status, TwitterError, Url, User

from config import (
    APP_KEY,
    APP_SECRET,
    CHECKED_STATUSES_DIR_PATH,
    LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME,
    LIST_OF_STATUS_IDS_REPLIED_TO,
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET,
    TEST_JSON_FILE_NAME,
    TEMP_JSON_FILE_NAME,
    TWITTER_API_USER,
)
from _logger import LOGGER
from wrapped_tweet import Tweet
from util import add_status_id_to_file, add_status_id_to_file_new, fetch_test_data_file


twitter_api = Api(
    consumer_key=APP_KEY,
    consumer_secret=APP_SECRET,
    access_token_key=OAUTH_TOKEN,
    access_token_secret=OAUTH_TOKEN_SECRET,
)


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


def get_status(status_id: Union[int, str]) -> Status:
    """Get tweet from api and return Tweet object"""
    LOGGER.info(f"twitter_api.GetStatus(status_id={status_id})")
    response = twitter_api.GetStatus(status_id=status_id)
    return response


def get_status_from_url(url: str) -> Status:
    """Get tweet from api and return Status object

    Args:
        url: url of the tweet

    Examples:
        * https://twitter.com/briebriejoy/status/1222711763248078849
    """
    LOGGER.info(f"Fetching tweet: {url}")
    f_url = furl(url)
    status_id = f_url.path.segments[-1]
    response = get_status(status_id=status_id)
    return response


def get_tweet_from_url(url: str) -> Tweet:
    """Get tweet from api and return Tweet object

    Args:
        url: url of the tweet

    Examples:
        * https://twitter.com/briebriejoy/status/1222711763248078849

    """
    response = get_status_from_url(url=url)
    return Tweet(response)


def get_all_users_tweets(twitter_user: str) -> List[Status]:
    """Helper method to collect ALL of a user's tweets

    Notes:
        Endpoint Resource family Requests / window (user auth) Requests / window (app auth)
        * GET statuses/user_timeline	statuses	900	1500
    """
    LOGGER.info(f"Getting tweets for user: {twitter_user}")
    user_tweet_count = twitter_api.GetUser(screen_name=twitter_user).statuses_count

    if int(user_tweet_count) > 3000:
        raise Exception("Whatever the hourly rate limit would be raise error for now")

    all_tweets = []

    initial_tweets = twitter_api.GetUserTimeline(screen_name=twitter_user, count=200)

    last_tweet_id = initial_tweets[-1].id
    all_tweets.extend(initial_tweets)

    for _ in range(int(user_tweet_count / 200)):
        new_tweets = twitter_api.GetUserTimeline(
            screen_name=twitter_user, max_id=last_tweet_id, count=200
        )
        all_tweets.extend(new_tweets)
        last_tweet_id = new_tweets[-1].id

    LOGGER.info(f"Found {len(all_tweets)} tweets for user {twitter_user}")
    return all_tweets


def get_recent_tweets_for_user(
    twitter_user: str, since_id: int = None, count: int = 10
) -> List[Status]:
    """Using Twitter API get recent tweets using user screen name"""
    LOGGER.debug(f"Getting last {count} tweets for user: {twitter_user}")
    return twitter_api.GetUserTimeline(
        screen_name=twitter_user, since_id=since_id, count=count
    )


def find_deleted_tweets(twitter_user: str) -> List[dict]:
    """Get list of tweets that were deleted"""
    bad_ids = []
    list_of_users_to_ignore = ["", ""]
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
    user_status_file_path = Path(CHECKED_STATUSES_DIR_PATH).joinpath(f"{user}.txt")
    last_status_id = check_for_last_status_id(file_name=user_status_file_path)

    try:
        user_tweets: List[Status] = get_recent_tweets_for_user(
            twitter_user=user, since_id=last_status_id
        )
        if user_tweets:
            LOGGER.debug(
                f"Found {len(user_tweets)} "
                f"{'tweets' if len(user_tweets) > 1 else 'tweet'} for {user}"
            )
            add_status_id_to_file_new(
                tweet_id=user_tweets[0].id_str, user_status_file=user_status_file_path
            )
        else:
            LOGGER.debug(f"No new tweets from {user} since {last_status_id}")
            return []
    except TwitterError as e:
        error_code = e.message[0].get("code")
        if error_code == 88:
            LOGGER.error(
                f"'Rate limit exceeded': unable to retrieve recent tweets for {user}"
            )
            sleep_time = 180
            LOGGER.error(f"Sleeping for {sleep_time} seconds")
            sleep(sleep_time)
        elif error_code == 326:
            LOGGER.error(
                f"'This account is temporarily locked, please login': "
                f"unable to retrieve recent tweets for {user}"
            )
        else:
            LOGGER.error(
                f"Something happened, unable to retrieve recent tweets for {user}: {e}"
            )
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
            add_status_id_to_file(
                tweet_id=str(tweet_reply_id),
                list_of_ids_replied_to_file_name=LIST_OF_STATUS_IDS_REPLIED_TO_FILE_NAME,
            )
    return True


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
            replied_to_tweet = Tweet(get_status(tweet.replied_to_status_id))
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


def save_user_test_data(file_name, user_name, count):
    """Make call with twitter api to get test data"""
    tweets = twitter_api.GetUserTimeline(screen_name=user_name, count=count)
    # maybe replace with map()
    clean_tweets = [s.AsDict() for s in tweets]
    with open(file_name, "w") as f:
        for t in clean_tweets:
            json.dump(t, f)


def save_all_user_data(user_name: str):
    """Make call with twitter api to get test data"""
    tweets = get_all_users_tweets(twitter_user=user_name)
    # maybe replace with map()
    clean_tweets = [s.AsDict() for s in tweets]
    with open(f"{user_name}_all_tweets.json", "w") as f:
        for t in clean_tweets:
            json.dump(t, f)


def save_tweet_test_data(file_name, status):
    """Make call with twitter api to get test data"""
    tweet = twitter_api.GetStatus(status_id=status)
    with open(file_name, "w") as f:
        json.dump(tweet.AsDict(), f)


def fetch_test_data(data_name):
    json_file = fetch_test_data_file(file_name=TEST_JSON_FILE_NAME)

    if type(json_file.get(data_name)) is list:
        return generate_mock_tweet(
            raw_status=[Status(**s) for s in json_file.get(data_name)]
        )
    else:
        return generate_mock_tweet(raw_status=Status(**json_file.get(data_name)))


def convert_dicts_in_status_to_obj(status: Status) -> Status:
    """Update each attribute of status with Twitter object"""
    keys_to_update = ["urls", "user", "user_mentions", "quoted_status"]
    for key in keys_to_update:
        if key == "urls":
            status.urls = [Url(**url) for url in status.__getattribute__(key)]
        elif key == "user":
            status.user = User(**status.__getattribute__(key))
        elif key == "user_mentions":
            status.user_mentions = [
                User(**user) for user in status.__getattribute__(key)
            ]
        elif key == "quoted_status":
            status.quoted_status = (
                convert_dicts_in_status_to_obj(
                    status=Status(**status.__getattribute__(key))
                )
                if status.__getattribute__(key)
                else None
            )
    return status


def generate_mock_tweet(
    raw_status: Union[Status, List[Status]]
) -> Union[Status, List[Status]]:
    """Return mocked tweet to be used in tests"""
    if type(raw_status) == list:
        updated_status = [
            generate_mock_tweet(raw_status=status) for status in raw_status
        ]
    else:
        updated_status = convert_dicts_in_status_to_obj(status=raw_status)

    return updated_status


if __name__ == "__main__":
    # uncomment to create test data
    # save_user_test_data(
    #     file_name=TEMP_JSON_FILE_NAME, user_name="timheidecker", count=20
    # )
    # save_tweet_test_data(file_name=TEMP_JSON_FILE_NAME, status=1215708312249028609)
    LOGGER.info("End of file")

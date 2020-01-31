import json
from typing import List, Union

from furl import furl
from twitter import Api as twitterApi, Status, TwitterError, Url, User

from config import (
    APP_KEY,
    APP_SECRET,
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


twitter_api = twitterApi(
    consumer_key=APP_KEY,
    consumer_secret=APP_SECRET,
    access_token_key=OAUTH_TOKEN,
    access_token_secret=OAUTH_TOKEN_SECRET,
)


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


def get_status_from_url(url: str) -> Status:
    """Get tweet from api and return Status object

    Args:
        url: url of the tweet

    Examples:
        * https://twitter.com/briebriejoy/status/1222711763248078849
    """
    LOGGER.info(f"Fetching status: {url}")
    f_url = furl(url)
    status_id = f_url.path.segments[-1]
    response = twitter_api.GetStatus(status_id=status_id)
    return response


def get_tweet(tweet_id: Union[int, str]) -> Tweet:
    """Get tweet from api and return Tweet object"""
    LOGGER.info(f"Fetching tweet with id {tweet_id}")
    response = get_status(status_id=tweet_id)
    return Tweet(response)


def get_tweet_from_url(url: str) -> Tweet:
    """Get tweet from api and return Tweet object

    Args:
        url: url of the tweet

    Examples:
        * https://twitter.com/briebriejoy/status/1222711763248078849

    """
    LOGGER.info(f"Fetching tweet: {url}")
    response = get_status_from_url(url=url)
    return Tweet(response)


def get_all_users_tweets(twitter_user: str) -> List[Tweet]:
    """Helper method to collect ALL of a user's tweets

    Notes:
        Endpoint Resource family Requests / window (user auth) Requests / window (app auth)
        * GET statuses/user_timeline	statuses	900	1500
    """
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
            elif tweet.user == tweet.quoted_tweet_user:
                LOGGER.debug(
                    f"Skipping tweet({tweet.quoted_tweet_id}) "
                    f"from @{tweet.user}'s tweet({tweet.id}) quotes their own tweet"
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


def save_user_test_data(file_name, user_name, count):
    """Make call with twitter api to get test data"""
    tweets = twitter_api.GetUserTimeline(screen_name=user_name, count=count)
    clean_tweets = [s.AsDict() for s in tweets]
    with open(file_name, "w") as f:
        for t in clean_tweets:
            json.dump(t, f)


def save_tweet_test_data(file_name, status):
    """Make call with twitter api to get test data"""
    tweet = twitter_api.GetStatus(status_id=status)
    with open(file_name, "w") as f:
        json.dump(tweet.AsDict(), f)


def fetch_test_data_file():
    with open(TEST_JSON_FILE_NAME, "r") as f:
        json_file = json.load(f)
    return json_file


def fetch_test_data(data_name):
    json_file = fetch_test_data_file()

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
    save_user_test_data(
        file_name=TEMP_JSON_FILE_NAME, user_name="timheidecker", count=20
    )

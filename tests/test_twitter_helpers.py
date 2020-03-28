"""test_twitter_helpers.py

Tests for all the helper functions from twitter_helpers.py
"""
from unittest.mock import patch

from twitter import Status

from twitter_helpers import (
    find_quoted_tweets,
    get_recent_quoted_retweets_for_user,
    get_recent_tweets_for_user,
    post_collected_tweets,
    post_reply_to_user_tweet,
)
from util import file_reader
from wrapped_tweet import Tweet


@patch("twitter.api.Api.GetUserTimeline")
def test_find_quoted_tweets_for_quoted_tweet(mock_get, test_status):
    """Verify find_quoted_tweets method returns Tweet

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    test_tweets = [test_status("quoted_tweet")]
    mock_get.return_value = test_tweets
    user_name = "_b_axe"
    tweets = find_quoted_tweets(user=user_name)
    tweet = tweets[0]
    assert len(tweets) == 1
    assert type(tweets) == list
    assert type(tweet) == Tweet
    assert tweet.user == user_name
    assert tweet.quoted_tweet_id == 1236824680239181825
    assert tweet.tweet_str == f"@{user_name}: {test_tweets[0].text}"
    assert tweet.quoted_status == test_tweets[0].quoted_status
    assert tweet.id == test_tweets[0].id


@patch("twitter.api.Api.GetUserTimeline")
def test_find_quoted_tweets_for_user_excluded(mock_get, test_status):
    """Verify find_quoted_tweets method returns None

    The find_quoted_tweets method returns None for a tweet that
    is in the excluded_ids list.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    mock_get.return_value = [test_status("replied_to_quoted_tweet")]
    user_name = "_b_axe"
    tweets = find_quoted_tweets(user=user_name)
    assert len(tweets) == 0
    assert type(tweets) == list


@patch("twitter.api.Api.GetUserTimeline")
def test_find_quoted_tweets_for_bot_tweet(mock_get, test_status):
    """Verify find_quoted_tweets method returns None

    The find_quoted_tweets method returns None for a tweet that
    is created by bot user.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    basic_tweet = test_status("quote_bot_status")
    mock_get.return_value = [basic_tweet]
    quoted_retweets = find_quoted_tweets(user="_b_axe")
    assert not quoted_retweets
    assert len(quoted_retweets) == 0
    assert type(quoted_retweets) == list


@patch("twitter.api.Api.GetUserTimeline")
def test_find_quoted_tweets_for_non_retweet(mock_get, test_status):
    """Verify find_quoted_tweets method returns None

    The find_quoted_tweets method returns None for a tweet that is not a retweet.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    basic_tweet = test_status("basic_tweet")
    mock_get.return_value = [basic_tweet]
    quoted_retweets = find_quoted_tweets(user="_b_axe")
    assert not quoted_retweets


@patch("twitter.api.Api.GetUserTimeline")
def test_find_quoted_tweets_for_users_own_tweet(mock_get, test_status):
    """Verify find_quoted_tweets method returns None

    The find_quoted_tweets method returns None for a tweet that
    quotes the user's own tweet.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    basic_tweet = test_status("quote_users_own_status")
    mock_get.return_value = [basic_tweet]
    quoted_retweets = find_quoted_tweets(user="_b_axe")
    assert not quoted_retweets
    assert len(quoted_retweets) == 0
    assert type(quoted_retweets) == list


@patch("twitter.api.Api.GetUserTimeline")
@patch("twitter.api.Api.GetStatus")
def test_find_quoted_tweets_for_tweeted_already_quoted_by_user(
    mock_get_user_time_line, mock_get_status, test_status
):
    """Verify find_quoted_tweets method returns None

    The find_quoted_tweets method returns None for a tweet that
    quotes a tweet that has already been quoted in same thread.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    basic_tweets = test_status("quoted_tweets_for_tweeted_already_quoted_by_user")
    mock_get_user_time_line.side_effect = basic_tweets
    mock_get_status.side_effect = [basic_tweets, basic_tweets[0]]
    quoted_retweets = find_quoted_tweets(user="_b_axe_")
    assert not quoted_retweets


@patch("twitter.api.Api.GetUserTimeline")
def test_get_recent_quoted_retweets_for_user_for_quoted_tweet(mock_get, test_status):
    """Verify get_recent_quoted_retweets_for_user method returns Tweet

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    mock_get.return_value = [test_status("quoted_tweet")]
    user_name = "_b_axe"
    tweets = get_recent_quoted_retweets_for_user(
        twitter_user=user_name,
        excluded_ids=["1218223881045139457", "1217726499781873664"],
    )
    assert len(tweets) == 1
    assert type(tweets) == list
    assert type(tweets[0]) == Tweet


@patch("twitter.api.Api.GetUserTimeline")
def test_get_recent_quoted_retweets_for_user_for_user_excluded(mock_get, test_status):
    """Verify get_recent_quoted_retweets_for_user method returns None

    The get_recent_quoted_retweets_for_user method returns None for a tweet that
    is in the excluded_ids list.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    mock_get.return_value = [test_status("quoted_tweet")]
    user_name = "_b_axe"
    tweets = get_recent_quoted_retweets_for_user(
        twitter_user=user_name, excluded_ids=["1236873389073141760"]
    )
    assert len(tweets) == 0
    assert type(tweets) == list


@patch("twitter.api.Api.GetUserTimeline")
def test_get_recent_quoted_retweets_for_user_for_bot_tweet(mock_get, test_status):
    """Verify get_recent_quoted_retweets_for_user method returns None

    The get_recent_quoted_retweets_for_user method returns None for a tweet that
    is created by bot user.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    basic_tweet = test_status("quote_bot_status")
    mock_get.return_value = [basic_tweet]
    quoted_retweets = get_recent_quoted_retweets_for_user(
        twitter_user="_b_axe",
        excluded_ids=["1218223881045139457", "1217726499781873664"],
    )
    assert not quoted_retweets


@patch("twitter.api.Api.GetUserTimeline")
def test_get_recent_quoted_retweets_for_user_for_non_retweet(mock_get, test_status):
    """Verify get_recent_quoted_retweets_for_user method returns None

    The get_recent_quoted_retweets_for_user method returns None for a tweet that
    is not a retweet.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    basic_tweet = test_status("basic_tweet")
    mock_get.return_value = [basic_tweet]
    quoted_retweets = get_recent_quoted_retweets_for_user(
        twitter_user="FTBandFTR",
        excluded_ids=["1218223881045139457", "1217726499781873664"],
    )
    assert not quoted_retweets


@patch("twitter.api.Api.GetUserTimeline")
def test_get_recent_quoted_retweets_for_user_for_users_own_tweet(mock_get, test_status):
    """Verify get_recent_quoted_retweets_for_user method returns None

    The get_recent_quoted_retweets_for_user method returns None for a tweet that
    quotes the user's own tweet.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    basic_tweet = test_status("quote_users_own_status")
    mock_get.return_value = [basic_tweet]
    quoted_retweets = get_recent_quoted_retweets_for_user(
        twitter_user="jvgraz",
        excluded_ids=["1218223881045139457", "1217726499781873664"],
    )
    assert not quoted_retweets


def test_tweet_expected_properties(test_status):
    """Verify Tweet instance returns expected value for listed properties"""
    basic_tweet = test_status("basic_tweet")
    tweet = Tweet(basic_tweet)
    assert type(tweet) == Tweet
    assert tweet.user == basic_tweet.user.screen_name
    assert tweet.id == basic_tweet.id
    assert tweet.id_str == basic_tweet.id_str
    assert tweet.text == basic_tweet.text
    assert tweet.replied_to_status_bool
    # Verify Status has been saved to raw_tweet property
    assert tweet.raw_tweet.user == basic_tweet.user
    assert tweet.raw_tweet.id == basic_tweet.id
    assert tweet.raw_tweet.id_str == basic_tweet.id_str
    assert tweet.raw_tweet.text == basic_tweet.text


def test_tweet_none_properties(test_status):
    """Verify Tweet instance returns None for the expected properties"""
    basic_tweet = test_status("basic_tweet")
    expected_none_properties = [
        "quoted_status",
        "quoted_tweet_id",
        "quoted_tweet_user",
        "quoted_tweet_url",
        "for_the_record_message",
        "urls_from_quoted_tweet",
    ]
    tweet = Tweet(basic_tweet)
    assert type(tweet) == Tweet
    non_none_properties = [
        name for name in expected_none_properties if tweet.__getattribute__(name)
    ]
    assert not non_none_properties


@patch("twitter.api.Api.GetUserTimeline")
def test_get_recent_tweets_for_user(mock_get, test_status):
    basic_tweet = test_status("basic_tweet")
    mock_get.return_value = [basic_tweet]
    tweets = get_recent_tweets_for_user(twitter_user="FTBandFTR", count=10)
    assert all(type(t) is Status for t in tweets)


@patch("twitter.api.Api.PostUpdate")
def test_post_reply_to_user_tweet(mock_get, test_status):
    """Verify post_reply_to_user_tweet method returns tweet

    Notes:
       * Mock PostUpdate without making real call to Twitter API
    """
    quoted_tweet = test_status("reply_to_quoted_tweet")
    mock_get.return_value = quoted_tweet
    response = post_reply_to_user_tweet(tweet=Tweet(quoted_tweet))
    assert response.id == 1236873389073141760
    assert response.id_str == "1236873389073141760"
    assert response.quoted_status.id == 1236824680239181825
    assert type(response) == Status


@patch("twitter.api.Api.PostUpdate")
def test_post_collected_tweets(mock_get, test_status):
    """Verify post_collected_tweets method returns None

    Notes:
       * Mock PostUpdate without making real call to Twitter API
    """
    from os import path

    expected_num_of_ids = 3

    status_id_file_name = path.join(
        path.dirname(__file__), "../list_of_status_ids_replied_to.txt"
    )
    list_of_status_ids_replied_to = list(file_reader(status_id_file_name))
    assert len(list_of_status_ids_replied_to) == expected_num_of_ids, (
        f"Expected number ({expected_num_of_ids}) of status ids replied to "
        f"did not match actual ({len(list_of_status_ids_replied_to)})"
    )
    quoted_tweet = test_status("post_reply_response")
    mock_get.return_value = quoted_tweet
    response = post_collected_tweets(quoted_tweets=[Tweet(quoted_tweet)])
    new_list_of_status_ids_replied_to = list(file_reader(status_id_file_name))
    assert (
        str(quoted_tweet.in_reply_to_status_id) == new_list_of_status_ids_replied_to[-1]
    ), "Expected status id to be last item in list"
    assert response
    # clean up by overwriting file with original list
    with open(status_id_file_name, "w") as f:
        for line in list_of_status_ids_replied_to:
            f.write(line + "\n")


def test_tweet_quoted_tweet(test_status):
    expected_user = "jimcramer"
    expected_id = 1236824680239181825
    tweet = Tweet(test_status("quoted_tweet"))
    assert type(tweet.quoted_status) == Status
    assert tweet.quoted_tweet_user == expected_user
    assert tweet.quoted_tweet_id == expected_id
    assert tweet.quoted_tweet_locator == f"div[data-tweet-id='{expected_id}']"
    assert (
        tweet.quoted_tweet_url
        == f"https://twitter.com/{expected_user}/status/{expected_id}"
    )
    assert tweet.tweet_locator == f"div[data-tweet-id='1236873389073141760']"
    assert tweet.for_the_record_message == (
        "@_b_axe This Tweet is available! \n"
        "For the blocked and the record!\n"
        "URL(s) from tweet: https://t.co/wQw2axvaY9"
    )
    assert tweet.urls_from_quoted_tweet == ["https://t.co/wQw2axvaY9"]
    assert tweet.__repr__() == "@_b_axe: #FTR https://t.co/VPPbd36BbX"


@patch("twitter.api.Api.GetUserTimeline")
def test_get_one_recent_tweets_for_user(mock_get, test_status):
    """Verify get_recent_tweets_for_user method returns tweet

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    mock_get.return_value = test_status("mocked_status")
    user_name = "FTBandFTR"
    user_tweets = get_recent_tweets_for_user(twitter_user=user_name, count=1)
    assert len(user_tweets) == 1
    assert type(user_tweets) == list
    assert type(user_tweets[0]) == Status

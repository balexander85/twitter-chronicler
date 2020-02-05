"""test_twitter_helpers.py

Tests for all the helper functions from twitter_helpers.py
"""
from unittest.mock import patch

from twitter_helpers import find_quoted_tweets, get_recent_quoted_retweets_for_user
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
    tweets = find_quoted_tweets(users_to_follow=[user_name])
    assert len(tweets) == 1
    assert type(tweets) == list
    assert type(tweets[0]) == Tweet


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
    tweets = find_quoted_tweets(users_to_follow=[user_name])
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
    quoted_retweets = find_quoted_tweets(users_to_follow=["_b_axe"])
    assert not quoted_retweets


@patch("twitter.api.Api.GetUserTimeline")
def test_find_quoted_tweets_for_non_retweet(mock_get, test_status):
    """Verify find_quoted_tweets method returns None

    The find_quoted_tweets method returns None for a tweet that is not a retweet.

    Notes:
       * Mock GetUserTimeline without making real call to Twitter API
    """
    basic_tweet = test_status("basic_tweet")
    mock_get.return_value = [basic_tweet]
    quoted_retweets = find_quoted_tweets(users_to_follow=["_b_axe"])
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
    quoted_retweets = find_quoted_tweets(users_to_follow=["jvgraz"])
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
        twitter_user=user_name, excluded_ids=["1201197107169898498"]
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

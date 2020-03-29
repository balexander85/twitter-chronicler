"""test_twitter_helpers.py

Tests for all the helper functions from twitter_helpers.py
"""
from unittest.mock import patch

from twitter import Status

from twitter_helpers import (
    find_quoted_tweets,
    get_recent_tweets_for_user,
    post_collected_tweets,
    post_reply_to_user_tweet,
    process_tweet,
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

    expected_num_of_ids = 4

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
    test_tweet = test_status("quoted_tweet")
    expected_user = test_tweet.quoted_status.user.screen_name
    expected_replied_to_user = test_tweet.quoted_status.in_reply_to_screen_name
    expected_quoted_status_text = test_tweet.quoted_status.text.replace(
        f"@{expected_replied_to_user} ", f'@{expected_replied_to_user} "'
    )
    expected_id = test_tweet.quoted_status.id
    tweet = Tweet(test_tweet)
    assert type(tweet.quoted_status) == Status
    assert tweet.quoted_tweet_user == expected_user
    assert tweet.quoted_tweet_id == expected_id
    assert tweet.quoted_tweet_locator == f"div[data-tweet-id='{expected_id}']"
    assert (
        tweet.quoted_tweet_url
        == f"https://twitter.com/{expected_user}/status/{expected_id}"
    )
    assert tweet.tweet_locator == f"div[data-tweet-id='{test_tweet.id}']"
    assert (
        tweet.for_the_record_message
        == f'@{tweet.user} "{expected_quoted_status_text}" -.@{expected_user}'
    )
    assert tweet.urls_from_quoted_tweet == [
        url_obj.url for url_obj in test_tweet.quoted_status.urls
    ]
    assert tweet.__repr__() == f"@{test_tweet.user.screen_name}: {test_tweet.text}"


def test_tweet_quoted_a_reply_to_tweet(test_status):
    test_tweet = test_status("quoted_a_reply_to")
    expected_user = test_tweet.quoted_status.user.screen_name
    expected_replied_to_user = test_tweet.quoted_status.in_reply_to_screen_name
    expected_quoted_status_text = test_tweet.quoted_status.text.replace(
        f"@{expected_replied_to_user} ", f'@{expected_replied_to_user} "'
    )
    expected_id = test_tweet.quoted_status.id
    tweet = Tweet(test_tweet)
    assert type(tweet.quoted_status) == Status
    assert tweet.quoted_tweet_user == expected_user
    assert tweet.quoted_tweet_id == expected_id
    assert tweet.quoted_tweet_locator == f"div[data-tweet-id='{expected_id}']"
    assert (
        tweet.quoted_tweet_url
        == f"https://twitter.com/{expected_user}/status/{expected_id}"
    )
    assert tweet.tweet_locator == f"div[data-tweet-id='{test_tweet.id}']"
    assert (
        tweet.for_the_record_message
        == f'{expected_quoted_status_text}" -.@{expected_user}'
    )
    assert tweet.urls_from_quoted_tweet == [
        url_obj.url for url_obj in test_tweet.quoted_status.urls
    ]
    assert tweet.__repr__() == f"@{test_tweet.user.screen_name}: {test_tweet.text}"


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


def test_process_tweet_for_quoted_tweet(test_status):
    """Verify process_tweet method returns Tweet"""
    test_tweet = test_status("quoted_tweet")
    tweet = process_tweet(
        status=test_tweet, excluded_ids=["1218223881045139457", "1217726499781873664"],
    )
    assert type(tweet) == Tweet


def test_process_tweet_from_excluded_list(test_status):
    """Verify process_tweet method returns None

    The process_tweet method returns None for a tweet that is in the excluded_ids list.
    """
    test_tweet = test_status("quoted_tweet")
    tweet = process_tweet(status=test_tweet, excluded_ids=["1236873389073141760"])
    assert not tweet


def test_process_tweet_for_bot_tweet(test_status):
    """Verify process_tweet method returns None

    The process_tweet method returns None for a tweet that is created by bot user.
    """
    test_tweet = test_status("quote_bot_status")
    tweet = process_tweet(status=test_tweet)
    assert not tweet


def test_process_tweet_for_tweet_already_quoted_by_user(test_status):
    """Verify process_tweet method returns None

    The process_tweet method returns None for a tweet that
    quotes a tweet that has already been quoted in same thread.
    """
    test_tweet = test_status("quoted_tweets_for_tweeted_already_quoted_by_user")
    tweet = process_tweet(status=test_tweet, excluded_ids=["1243010309067071489"])
    assert not tweet


def test_process_tweet_for_tweet_with_none_reply_status_id(test_status):
    """Verify process_tweet method returns tweet"""
    test_tweet = test_status("basic_quoted_tweet")
    tweet = process_tweet(status=test_tweet)

    assert type(tweet) == Tweet
    assert not tweet.replied_to_status_id
    assert tweet.user == test_tweet.user.screen_name
    assert tweet.quoted_tweet_id == test_tweet.quoted_status.id
    assert tweet.tweet_str == f"@{test_tweet.user.screen_name}: {test_tweet.text}"
    assert tweet.quoted_status == test_tweet.quoted_status
    assert tweet.id == test_tweet.id


def test_process_tweet_for_user_for_non_retweet(test_status):
    """Verify get_recent_quoted_retweets_for_user method returns None

    The process_tweet method returns None for a tweet that is not a retweet.
    """
    test_tweet = test_status("basic_tweet")
    quoted_retweets = process_tweet(
        status=test_tweet, excluded_ids=["1218223881045139457", "1217726499781873664"],
    )
    assert not quoted_retweets


def test_process_tweet_for_user_for_users_own_tweet(test_status):
    """Verify process_tweet method returns None

    The process_tweet method returns None for a tweet that quotes the user's own tweet.
    """
    test_tweet = test_status("quote_users_own_status")
    quoted_retweets = process_tweet(
        status=test_tweet, excluded_ids=["1218223881045139457", "1217726499781873664"],
    )
    assert not quoted_retweets

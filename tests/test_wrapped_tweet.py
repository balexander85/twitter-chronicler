"""test_wrapped_tweet.py

Tests for Tweet class from the wrapped_tweet module
"""
from twitter import Status

from wrapped_tweet import Tweet


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


# Future tests below - tests above to be removed or replaced


def test_tweet_quoted_no_reply_with_image_and_no_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_no_reply_with_image_and_no_text")


def test_tweet_quoted_no_reply_with_image_and_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_no_reply_with_image_and_text")


def test_tweet_quoted_no_reply_with_mentions_and_no_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_no_reply_with_mentions_and_no_text")


def test_tweet_quoted_no_reply_with_mentions_and_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_no_reply_with_mentions_and_text")


def test_tweet_quoted_single_user_reply_with_image_and_no_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_single_user_reply_with_image_and_no_text")


def test_tweet_quoted_single_user_reply_with_image_and_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_single_user_reply_with_image_and_text")


def test_tweet_quoted_single_user_reply_with_mentions_and_no_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_single_user_reply_with_mentions_and_no_text")


def test_tweet_quoted_single_user_reply_with_mentions_and_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_single_user_reply_with_mentions_and_text")
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


def test_tweet_quoted_multiple_user_reply_with_image_and_no_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_multiple_user_reply_with_image_and_no_text")
    expected_user = test_tweet.quoted_status.user.screen_name
    expected_replied_to_user = test_tweet.quoted_status.in_reply_to_screen_name
    expected_quoted_status_text = test_tweet.quoted_status.text.replace(
        f"@{expected_replied_to_user} ", ""
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


def test_tweet_quoted_multiple_user_reply_with_image_and_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_multiple_user_reply_with_image_and_text")


def test_tweet_quoted_multiple_user_reply_with_mentions_and_no_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_multiple_user_reply_with_mentions_and_no_text")


def test_tweet_quoted_multiple_user_reply_with_mentions_and_text(test_status):
    """Verify Tweet()"""
    test_tweet = test_status("quoted_multiple_user_reply_with_mentions_and_text")

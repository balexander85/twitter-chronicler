import pytest
from unittest.mock import patch

from user_requests import search_for_requests
from wrapped_tweet import Tweet


@patch("twitter.api.Api.GetMentions")
@pytest.mark.skip("Not implemented")
def test_search_for_requests(mock_get, test_status):
    test_request = test_status("test_request")
    mock_get.return_value = [test_request]
    tweets = search_for_requests()
    assert len(tweets) == 1
    assert all(type(t) is Tweet for t in tweets)


@patch("twitter.api.Api.GetMentions")
@pytest.mark.skip("Not implemented")
def test_search_for_requests_non_request(mock_get, test_status):
    basic_tweet = test_status("basic_tweet")
    mock_get.return_value = [basic_tweet]
    tweet_ids = search_for_requests()
    assert len(tweet_ids) == 0

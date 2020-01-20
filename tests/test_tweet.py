from unittest.mock import patch

import pytest
from twitter import Status

from twitter_helpers import (
    get_tweet,
    get_recent_tweets_for_user,
    post_collected_tweets,
    post_reply_to_user_tweet,
    Tweet,
)


@pytest.mark.skip
class TestGetTweet:
    def test_get_tweet_int(self):
        """Verify get_tweet method returns Tweet object"""
        tweet_id_int = 1201197107169898498
        tweet = get_tweet(tweet_id=tweet_id_int)
        assert type(tweet) == Tweet
        assert tweet.id == tweet_id_int

    def test_get_tweet_str(self):
        """Verify get_tweet method returns Tweet object"""
        tweet_id_str = f"{1201197107169898498}"
        tweet = get_tweet(tweet_id=tweet_id_str)
        assert type(tweet) == Tweet
        assert tweet.id_str == tweet_id_str


class TestTweet:
    """
    Verify functionality related to Tweet object
    and other helper methods from twitter_helpers.py
    """

    def test_basic_tweet(self, test_tweet):
        """Verify get_tweet method returns Tweet object"""
        tweet = Tweet(test_tweet("basic_tweet"))
        assert type(tweet) == Tweet
        assert tweet.user == "FTBandFTR"
        assert tweet.id == 1206058311864528896
        assert tweet.id_str == "1206058311864528896"
        assert (
            tweet.text
            == "If someone wants off the list that’s okay. I will remove them ASAP."
        )
        assert tweet.replied_to_status_bool
        assert tweet.__repr__() == (
            "@FTBandFTR: If someone wants off the list that’s okay. I will remove them "
            "ASAP."
        )

    def test_quoted_tweet(self, test_tweet):
        file_path_quoted_tweet = (
            "/Users/brian/Development/repos/"
            "projects_github/twitter_chronicler/screen_shots/"
        )
        file_name_quoted_tweet = "tweet_capture_1200946238033661957.png"
        expected_user = "WajahatAli"
        expected_id = 1200946238033661957
        tweet = Tweet(test_tweet("quoted_tweet"))
        assert type(tweet.quoted_status) == Status
        assert tweet.quoted_tweet_user == expected_user
        assert tweet.quoted_tweet_id == expected_id
        assert tweet.quoted_tweet_locator == f"div[data-tweet-id='{expected_id}']"
        assert tweet.screen_capture_file_name_quoted_tweet == file_name_quoted_tweet
        assert (
            tweet.screen_capture_file_path_quoted_tweet
            == f"{file_path_quoted_tweet}{file_name_quoted_tweet}"
        )
        assert (
            tweet.quoted_tweet_url
            == f"https://twitter.com/{expected_user}/status/{expected_id}"
        )
        assert tweet.tweet_locator == f"div[data-tweet-id='1201197107169898498']"
        assert tweet.for_the_record_message == (
            "@_b_axe "
            "This Tweet is available! \n"
            "For the blocked and the record!\n"
            "URL(s) from tweet: https://t.co/AlQY448xZs"
        )
        assert tweet.urls_from_quoted_tweet == ["https://t.co/AlQY448xZs"]
        assert tweet.__repr__() == (
            "@_b_axe: @WajahatAli Why exclude Tulsi? https://t.co/1tHcDRwFSj "
            "https://t.co/qc3x1ro2PT"
        )

    @patch("twitter.api.Api.GetUserTimeline")
    def test_get_one_recent_tweets_for_user(self, mock_get, test_tweet):
        """Mock get_recent_tweets_for_user without making real call to Twitter API"""
        mock_get.return_value = test_tweet("mock_status")
        user_name = "FTBandFTR"
        user_tweets = get_recent_tweets_for_user(twitter_user=user_name, count=1)
        assert len(user_tweets) == 1
        assert type(user_tweets) == list

    @patch("twitter.api.Api.PostUpdate")
    def test_post_reply_to_user_tweet(self, mock_get, test_tweet):
        """Mock post_reply_to_user_tweet without making real call to Twitter API"""
        quoted_tweet = test_tweet("quoted_tweet")
        mock_get.return_value = quoted_tweet
        response = post_reply_to_user_tweet(tweet=Tweet(quoted_tweet))
        assert response.id == 1201197107169898498
        assert response.id_str == "1201197107169898498"
        assert response.quoted_status.id == 1200946238033661957
        assert type(response) == Status

    @patch("twitter.api.Api.PostUpdate")
    def test_post_collected_tweets(self, mock_get, test_tweet):
        """Mock post_reply_to_user_tweet without making real call to Twitter API"""
        quoted_tweet = test_tweet("quoted_tweet")
        mock_get.return_value = quoted_tweet
        response = post_collected_tweets(quoted_tweets=[Tweet(quoted_tweet)])
        assert not response

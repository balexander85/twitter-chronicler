from unittest.mock import patch

import pytest
from twitter import Status

from config import (
    LIST_OF_USERS_TO_FOLLOW,
    LIST_OF_STATUS_IDS_REPLIED_TO,
)
from twitter_helpers import (
    find_quoted_tweets,
    get_tweet,
    get_recent_quoted_retweets_for_user,
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
        mock_get.return_value = test_tweet("mocked_status")
        user_name = "FTBandFTR"
        user_tweets = get_recent_tweets_for_user(twitter_user=user_name, count=1)
        assert len(user_tweets) == 1
        assert type(user_tweets) == list

    @patch("twitter_helpers.get_recent_tweets_for_user")
    def test_get_recent_quoted_retweets_for_user_excluded(self, mock_get, test_tweet):
        """Mock get_recent_tweets_for_user without making real call to Twitter API"""
        mock_get.return_value = [test_tweet("quoted_tweet")]
        user_name = "_b_axe"
        tweets = get_recent_quoted_retweets_for_user(
            twitter_user=user_name, excluded_ids=["1201197107169898498"]
        )
        assert len(tweets) == 0
        assert type(tweets) == list

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

    # @patch("twitter_helpers.get_recent_tweets_for_user")
    # def test_find_quoted_tweets_quote_bot_user(self, mock_get, test_tweet):
    #     """Verify find_quoted_tweets method returns None for tweet by bot"""
    #     basic_tweet = test_tweet("quote_bot_status")
    #     mock_get.return_value = [basic_tweet]
    #     quoted_retweets = find_quoted_tweets(users_to_follow=["FTBandFTR"])
    #     assert not quoted_retweets

    # @patch("twitter_helpers.get_recent_tweets_for_user")
    # def test_get_recent_quoted_retweets_for_user_quote_bot_user(
    #     self, mock_get, test_tweet
    # ):
    #     """Verify find_quoted_tweets method returns None for tweet by bot"""
    #     basic_tweet = test_tweet("quote_bot_status")
    #     mock_get.return_value = [basic_tweet]
    #     quoted_retweets = get_recent_quoted_retweets_for_user(
    #         twitter_user="_b_axe",
    #         excluded_ids=["1218223881045139457", "1217726499781873664"],
    #     )
    #     assert not quoted_retweets


class TestBasicTweet:
    """
    Verify functionality for basic tweets (non-retweets) related to
    Tweet object and other helper methods from twitter_helpers.py
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_tweet):
        self.basic_tweet = test_tweet("basic_tweet")

    def test_expected_properties(self):
        """Verify Tweet instance returns expected value for listed properties"""
        tweet = Tweet(self.basic_tweet)
        assert type(tweet) == Tweet
        assert tweet.user == self.basic_tweet.user.screen_name
        assert tweet.id == self.basic_tweet.id
        assert tweet.id_str == self.basic_tweet.id_str
        assert tweet.text == self.basic_tweet.text
        assert tweet.replied_to_status_bool
        # Verify Status has been saved to raw_tweet property
        assert tweet.raw_tweet.user == self.basic_tweet.user
        assert tweet.raw_tweet.id == self.basic_tweet.id
        assert tweet.raw_tweet.id_str == self.basic_tweet.id_str
        assert tweet.raw_tweet.text == self.basic_tweet.text

    def test_none_properties(self):
        """Verify Tweet instance returns None for the expected properties"""
        expected_none_properties = [
            "quoted_status",
            "quoted_tweet_id",
            "quoted_tweet_user",
            "quoted_tweet_url",
            "for_the_record_message",
            "screen_capture_file_name_quoted_tweet",
            "screen_capture_file_path_quoted_tweet",
            "urls_from_quoted_tweet",
        ]
        tweet = Tweet(self.basic_tweet)
        assert type(tweet) == Tweet
        non_none_properties = [
            name for name in expected_none_properties if tweet.__getattribute__(name)
        ]
        assert not non_none_properties

    @patch("twitter_helpers.get_recent_tweets_for_user")
    def test_find_quoted_tweets(self, mock_get):
        """Verify find_quoted_tweets method returns None for non-retweet"""
        mock_get.return_value = [self.basic_tweet]
        quoted_retweets = find_quoted_tweets(users_to_follow=["FTBandFTR"])
        assert not quoted_retweets

    @patch("twitter_helpers.get_recent_tweets_for_user")
    def test_get_recent_quoted_retweets_for_user(self, mock_get):
        """
        Verify get_recent_quoted_retweets_for_user method returns None for non-retweet
        """
        mock_get.return_value = [self.basic_tweet]
        quoted_retweets = get_recent_quoted_retweets_for_user(
            twitter_user="FTBandFTR",
            excluded_ids=["1218223881045139457", "1217726499781873664"],
        )
        assert not quoted_retweets

    @patch("twitter.api.Api.GetUserTimeline")
    def test_get_recent_tweets_for_user(self, mock_get):
        mock_get.return_value = [self.basic_tweet]
        tweets = get_recent_tweets_for_user(twitter_user="FTBandFTR", count=10,)
        assert all(type(t) is Status for t in tweets)

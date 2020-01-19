from unittest.mock import patch

from twitter import Status

from twitter_helpers import (
    get_tweet,
    Tweet,
    get_recent_tweets_for_user,
    post_reply_to_user_tweet,
)


class TestGetTweet:
    def test_get_tweet_int(self):
        """Verify get_tweet method returns Tweet object"""
        tweet_id_int = 1206058311864528896
        tweet = get_tweet(tweet_id=tweet_id_int)
        assert type(tweet) == Tweet
        assert tweet.id == tweet_id_int

    def test_get_tweet_str(self):
        """Verify get_tweet method returns Tweet object"""
        tweet_id_str = f"{1218642707586977797}"
        tweet = get_tweet(tweet_id=tweet_id_str)
        assert type(tweet) == Tweet
        assert tweet.id_str == tweet_id_str


class TestTweet:
    def test_basic_tweet(self, basic_tweet):
        """Verify get_tweet method returns Tweet object"""
        tweet = Tweet(basic_tweet)
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

    def test_quoted_tweet(self, quoted_tweet):
        file_path_quoted_tweet = (
            "/Users/brian/Development/repos/"
            "projects_github/twitter_chronicler/screen_shots/"
        )
        file_name_quoted_tweet = "tweet_capture_1218638650726146050.png"
        tweet = Tweet(quoted_tweet)
        assert type(tweet.quoted_status) == Status
        assert tweet.quoted_tweet_user == "kenklippenstein"
        assert tweet.quoted_tweet_id == 1218638650726146050
        assert tweet.quoted_tweet_locator == "div[data-tweet-id='1218638650726146050']"
        assert tweet.screen_capture_file_name_quoted_tweet == file_name_quoted_tweet
        assert (
            tweet.screen_capture_file_path_quoted_tweet
            == f"{file_path_quoted_tweet}{file_name_quoted_tweet}"
        )
        assert (
            tweet.quoted_tweet_url
            == "https://twitter.com/kenklippenstein/status/1218638650726146050"
        )
        assert tweet.tweet_locator == "div[data-tweet-id='1218642707586977797']"
        assert tweet.for_the_record_message == (
            "@ggreenwald "
            "This Tweet is available! \n"
            "For the blocked and the record!\n"
            "URL(s) from tweet: https://t.co/2kzeCWezvw"
        )
        assert tweet.urls_from_quoted_tweet == ["https://t.co/2kzeCWezvw"]
        assert tweet.__repr__() == (
            "@ggreenwald: Keep up the great work, MSNBC! \ud83d\udc4d "
            "https://t.co/eLAGZdirf9"
        )

    @patch("twitter.api.Api.GetUserTimeline")
    def test_get_one_recent_tweets_for_user(self, mock_get, mock_status):
        """Mock get_recent_tweets_for_user without making real call to Twitter API"""
        mock_get.return_value = mock_status
        user_name = "FTBandFTR"
        user_tweets = get_recent_tweets_for_user(twitter_user=user_name, count=1)
        assert len(user_tweets) == 1
        assert type(user_tweets) == list

    @patch("twitter.api.Api.PostUpdate")
    def test_post_reply_to_user_tweet(self, mock_get, quoted_tweet):
        """Mock post_reply_to_user_tweet without making real call to Twitter API"""
        mock_get.return_value = quoted_tweet
        response = post_reply_to_user_tweet(tweet=Tweet(quoted_tweet))
        assert response

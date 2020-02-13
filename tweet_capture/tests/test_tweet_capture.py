"""test_tweet_capture.py"""
from tweet_capture import TweetCapture


def test_tweet_screen_shot_tweet(test_tweet):
    """
    Verify functionality tweet_capture module
    """
    tweet_id = 1215707826783498242
    test_tweet = test_tweet("replied_to_quoted_tweet")
    with TweetCapture() as tweet_capture:
        screen_cap_file_path = tweet_capture.screen_shot_tweet(
            test_tweet.quoted_tweet_url
        )

    assert (
        screen_cap_file_path == "/Users/brian/Development/repos/projects_github/"
        "twitter_chronicler/tweet_capture/screen_shots/"
        f"tweet_capture_{tweet_id}.png"
    )


def test_tweet_capture_get_screen_capture_file_path_quoted_tweet(test_tweet):
    """
    Verify functionality tweet_capture module
    """
    tweet_id = 1215708312249028609
    assert (
        "/Users/brian/Development/repos/projects_github/twitter_chronicler"
        f"/tweet_capture/screen_shots/tweet_capture_{tweet_id}.png"
        == TweetCapture.get_screen_capture_file_path_quoted_tweet(tweet_id=tweet_id)
    )

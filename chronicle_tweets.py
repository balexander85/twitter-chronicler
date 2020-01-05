"""chronicle_tweets.py

Containing some helpful objects

1. List of users to follow
2. for each user watch for retweets that quote tweets
3. save screenshot of quoted tweet
4. save URL(s) from quoted tweet
5. Reply to tweet with image of quoted tweet with URL(s) and a disclaimer

This Tweet is available!

Note:
    I was tired of looking at tweets that quoted tweets
    where the quoted tweets had been deleted.
"""
from config import (
    LIST_OF_USERS_TO_FOLLOW,
    LIST_OF_STATUS_IDS_REPLIED_TO,
)
from wrapped_driver import WrappedWebDriver
from util import (
    LOGGER,
    get_users_recent_quoted_retweets,
    collect_quoted_tweets,
    post_collected_tweets,
)

if __name__ == "__main__":

    user_quoted_retweets = [
        tweets
        for user in LIST_OF_USERS_TO_FOLLOW
        for tweets in get_users_recent_quoted_retweets(
            twitter_user=user, excluded_ids=LIST_OF_STATUS_IDS_REPLIED_TO
        )
    ]
    if user_quoted_retweets:
        webdriver = WrappedWebDriver(browser="headless")
        collect_quoted_tweets(driver=webdriver, quoted_tweets=user_quoted_retweets)
        webdriver.quit_driver()
        post_collected_tweets(user_quoted_retweets)
    else:
        LOGGER.info(msg=f"No new retweets for users: {LIST_OF_USERS_TO_FOLLOW}")

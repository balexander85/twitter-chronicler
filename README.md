# twitter-chronicler

Scan user's recent tweets (10) for retweets that quote a tweet. For
each tweet that is quoted by user (exceptions apply), screen capture
the quoted tweet and reply to user with a screenshot of quoted tweet.


### Exceptions
* Retweet has already been replied to
* Retweet that quotes the user's own tweet
* Retweet that quotes a tweet that is created by bot user
* Retweet that quotes the same tweet that was quoted in same thread

### Notes
* I created this because I was tired of looking at tweets that
  quoted tweets where the quoted tweets had been deleted.

* The quoted tweet with the screenshot should include as much text
  from the tweet as possible so that users that have screen readers
  can have some clue as to the text of the quoted tweet.

* If a user starts a thread by quoting a tweet and then later in
  the thread the user quotes a different tweet both tweets should
  be collected.

* If user blocks the bot or their account is private or suspended
  then skip collection

### To be implemented
* Handle error if user blocks bot or their account is private or suspended
* Collect tweet if user quotes tweet where the user of the quoted tweet
  blocks the bot
* Send notification if user blocks bot or their account is private or suspended
* Add ability for user to request a tweet be screen capped
* Add ability for user to request screenshot of a tweet that is quoted by user
  where the user of the quoted tweet blocked the requesting user
* Keep track of number of twitter api calls made

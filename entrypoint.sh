#!/usr/bin/env bash

# Start the run once job.
echo "Docker container has been started"

# Setup a cron schedule
echo "* * * * * /usr/local/bin/python /usr/src/twitter_chronicler/runner.py >> /var/log/cron.log 2>&1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f

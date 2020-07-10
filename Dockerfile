FROM python:3.7-slim-buster
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src/twitter_chronicler
COPY _logger.py \
  config.py \
  chronicler.py \
  README.md \
  requirements.txt \
  runner.py \
  twitter_helpers.py \
  wrapped_tweet.py \
  util.py \
  entrypoint.sh ./
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends --no-install-suggests ca-certificates \
 && update-ca-certificates \
 # Install tools for building
 && toolDeps="git aptitude" \
 && apt-get install -y --no-install-recommends --no-install-suggests $toolDeps \
 # Install chromedriver and chromium with aptitude
 && aptitude install chromium-driver -y \
 # Install packages
 && apt-get install -y --no-install-recommends --no-install-suggests cron \
 && chmod +x ./entrypoint.sh \
 && pip install -r requirements.txt \
 && pip install -e git+https://github.com/balexander85/WrappedDriver.git#egg=WrappedDriver \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $toolDeps \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*
ENTRYPOINT ./entrypoint.sh

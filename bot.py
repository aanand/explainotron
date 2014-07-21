#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot

from extensions.sql_storage import SQLStorage
from extensions.explainer import Explainer

import random
import os
import logging


class Explainotron(TwitterBot):
    def bot_init(self):
        self.config['storage'] = SQLStorage(os.environ['DATABASE_URL'])

        self.config['api_key'] = os.environ['TWITTER_CONSUMER_KEY']
        self.config['api_secret'] = os.environ['TWITTER_CONSUMER_SECRET']
        self.config['access_key'] = os.environ['TWITTER_ACCESS_TOKEN']
        self.config['access_secret'] = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
        self.config['tweet_interval_range'] = (1*60, 3*60*60)

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = False

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = False

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = False

    def on_scheduled_tweet(self):
        text = self.generate_tweet(max_len=140)

        if self._is_silent():
            self.log("Silent mode is on. Would've tweeted: {}".format(text))
            return

        self.post_tweet(text)

    def on_mention(self, tweet, prefix):
        pass

    def on_timeline(self, tweet, prefix):
        pass

    def _is_silent(self):
        return int(os.environ.get('SILENT_MODE', '0')) != 0

    def generate_tweet(self, max_len):
        ex = Explainer(api=self.api)
        candidates = ex.generate(count=100)
        candidates = [c for c in candidates if len(c) <= max_len]

        if len(candidates) == 0:
            raise Exception("No suitable candidates were found")

        return random.choice(candidates)

if __name__ == '__main__':
    stderr = logging.StreamHandler()
    stderr.setLevel(logging.DEBUG)
    stderr.setFormatter(logging.Formatter(fmt='%(levelname)8s: %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stderr)

    bot = Explainotron()
    bot.run()

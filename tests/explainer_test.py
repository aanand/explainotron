from __future__ import unicode_literals
from unittest import TestCase

from extensions import explainer


class ExplainerTest(TestCase):
    def test_basic(self):
        tweets = [
            'explaining politics to my dad',
            'how to begin to explain my love \u2026',
        ]
        objects = [o for t in tweets for o in explainer.get_objects(t, explainer.Explainer.verbs)]
        self.assertEqual(list(objects), [
            'politics',
            'my love \u2026',
        ])

    def test_pronoun_ending(self):
        tweet = 'i cannot explain how beautiful he is'
        objects = explainer.get_objects(tweet, ['explain'])
        self.assertEqual(list(objects), [])

    def test_i(self):
        tweet = 'i cannot explain how beautiful i am'
        objects = explainer.get_objects(tweet, ['explain'])
        self.assertEqual(list(objects), [])

    def test_my(self):
        tweet = 'idk how to explain my feels towards you'
        objects = explainer.get_objects(tweet, ['explain'])
        self.assertNotIn('my', list(objects))

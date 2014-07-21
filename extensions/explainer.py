#!/usr/bin/env python

from __future__ import unicode_literals

import random

from pattern.en import parsetree


class Explainer(object):
    verbs = ["explain", "explained", "explaining"]

    def __init__(self, api):
        self.api = api

    def generate(self, count=1):
        subjects = list(set(self.get_things(self.verbs, self.verbs)))
        people = list(set(self.get_things(["talking to"], ["talking"])))

        if len(subjects) == 0:
            raise Exception("failed to get any subjects")

        if len(people) == 0:
            raise Exception("failed to get any people")

        for _ in range(count):
            yield self.explain(random.choice(subjects), random.choice(people))

    def explain(self, thing, person):
        return "How I Explained {} To {}".format(thing.title(), person.title())

    def get_things(self, terms, verbs):
        return [
            np
            for text in self.get_tweets(terms)
            for np in get_objects(text, verbs)
        ]

    def get_tweets(self, terms):
        query = " OR ".join('"{}"'.format(t) for t in terms)
        tweets = self.api.search(query, count=100, result_type="recent")
        tweets = [t.text for t in tweets]
        tweets = [t.replace('&amp;', 'and') for t in tweets]
        return tweets


def get_objects(text, verbs):
    """
    Given a passage of text and a list of verbs, yields all noun phrases
    which are at any point the object of any of those verbs.

    >>> list(get_objects("I'm explaining politics to my dad", ["explaining"]))
    ["politics"]

    >>> list(get_objects("I'm talking to my dad about politics", ["talking to"]))
    ["my dad"]
    """
    tree = parsetree(text)

    for sentence in tree:
        matching_verb_phrase_indices = [
            idx for idx, chunk in enumerate(sentence.chunks[:-1])
            if chunk.type == 'VP'
            and chunk.words[-1].string in verbs
        ]

        for idx in matching_verb_phrase_indices:
            chunk = sentence.chunks[idx+1]
            if chunk.type == 'NP':
                if accept_noun_phrase(chunk):
                    yield " ".join([w.string for w in chunk.words])


def accept_noun_phrase(chunk):
    if "http" in chunk.string.lower():
        return False
    if chunk.words[-1].type == 'PRP':
        return False
    if chunk.words[-1].string.lower() in ['i']:
        return False
    return True

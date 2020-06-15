import mnemonic
import itertools
from indy import main
from google.cloud import datastore
import asyncio
import time


def takeCoins():
    client = datastore.Client()
    key = client.key('seedWords', 5634161670881280)
    entity = client.get(key)
    possible_seeds = entity['possible_real']
    print(possible_seeds)

    # possible_seeds = ["attract" ,"what", "friend", "abandon"]

    num_permutations = 4
    num_words = len(possible_seeds.split())

    if (num_words) < 4 and (num_words) > 0:
        num_permutations = (num_words)
    m = mnemonic.Mnemonic('english')
    # TODO update this number accordingly
    perms = list(itertools.permutations(possible_seeds, num_permutations))

    valid_keys = []
    your8words = "army excuse hero wolf disease liberty moral diagram"

    for words in perms:
        key = your8words
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print('valid_phrases: ', valid_keys)
    main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)

    your8words = "army excuse hero wolf disease rebuild moral diagram"

    valid_keys = []
    for words in perms:
        key = your8words
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print(valid_keys)
    main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)

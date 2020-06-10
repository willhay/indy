import mnemonic
import itertools
from indy import main
from google.cloud import datastore
import asyncio


def takeCoins():
    # client = datastore.Client()
    # key = client.key('seedWords', 5634161670881280)
    # entity = client.get(key)
    # possible_seeds = entity['possible']
    # print(possible_seeds)

    # possible_seeds = ["attract" ,"what", "friend", "abandon"]
    # your8words1 = "army excuse hero wolf disease rebuild ability"
    # your8words2 = "army excuse hero wolf disease liberty ability"

    possible_seeds = ["grit", "rug", "girl", "baby"]
    m = mnemonic.Mnemonic('english')

    perms = list(itertools.permutations(possible_seeds, 4))
    valid_keys = []
    print(len(perms))
    your8words = "motor worry mean random pulse scan theme coffee"

    for words in perms:
        key = your8words
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print(valid_keys)
    main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)

    your8words = "motor worry mean random pulse disease theme coffee"

    valid_keys = []
    print(len(perms))
    for words in perms:
        key = your8words
        for word in words:
            key += ' ' + word
            key2 += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print(valid_keys)
    main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)


takeCoins()

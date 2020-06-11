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
    if len(possible_seeds) < 4 and len(possible_seeds) > 0:
        num_permuations = len(possible_seeds)
    m = mnemonic.Mnemonic('english')
    # TODO update this number accordingly
    perms = list(itertools.permutations(possible_seeds, num_permutations))

    valid_keys = []
    print(len(perms))
    # your8words = "army excuse hero wolf disease rebuild"
    your8words = "motor worry mean random pulse scan theme coffee"

    for words in perms:
        key = your8words
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print(valid_keys)
    main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)

    # your8words = "army excuse hero wolf disease liberty"
    your8words = "motor worry mean random pulse disease theme coffee"

    valid_keys = []
    print(len(perms))
    for words in perms:
        key = your8words
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print(valid_keys)
    main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)

while True:
    time.sleep(1)
    takeCoins()
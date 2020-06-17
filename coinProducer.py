import mnemonic
import itertools
from indy import main
from google.cloud import datastore
import asyncio
import time

m = mnemonic.Mnemonic('english')

client = datastore.Client()

def takeCoins():
    key = client.key('seedWords', 5634161670881280)
    entity = client.get(key)
    possible_seeds = entity['from_text']

    # possible_seeds = ['attract', 'swear', 'shrug', 'feel']

    num_permutations = 4
    num_words = len(possible_seeds)

    if (num_words) < 4 and (num_words) > 0:
        num_permutations = (num_words)
    perms = list(itertools.permutations(possible_seeds, num_permutations))

    valid_keys = []
    your8words = "army excuse hero wolf disease liberty moral diagram"
    # your8words = "banner frequent toe corn height escape finish sample"

    for words in perms:
        key = your8words
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print(valid_keys)
    if(valid_keys):
        main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)

    your8words = "army excuse hero wolf disease rebuild moral diagram"
    # your8words = "banner frequent toe corn height escape finish sample"

    valid_keys = []
    for words in perms:
        key = your8words
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print(valid_keys)
    if(valid_keys):
        main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)


while True:
    takeCoins()
    time.sleep(2)

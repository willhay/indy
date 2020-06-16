from google.cloud import datastore
import mnemonic
import itertools
from indy import main
import asyncio
import time


def takeCoins(last_seeds):

    # last_seeds = ["attract" ,"what", "friend", "abandon"]

    num_permutations = 4

    num_words = len(last_seeds.split())

    if (num_words) < 4 and (num_words) > 0:
        num_permutations = (num_words)
    m = mnemonic.Mnemonic('english')
    perms = list(itertools.permutations(last_seeds.split(), num_permutations))
    valid_keys = []
    phrase = "banner frequent toe corn height escape finish sample attract swear shrug"

    # phrase = "army excuse hero wolf disease liberty moral diagram"

    for words in perms:
        key = phrase
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print('valid_phrases: ', valid_keys)
    main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)
    phrase = "banner frequent toe corn height escape feel sample"

    # phrase = "army excuse hero wolf disease rebuild moral diagram"

    valid_keys = []
    for words in perms:
        key = phrase
        for word in words:
            key += ' ' + word
        if m.check(key):
            valid_keys.append(key)
    print('valid_phrases: ', valid_keys)
    main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', True)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--seeds',
                        help='path to dem')
    args = parser.parse_args()
    takeCoins(last_seeds=args.seeds)

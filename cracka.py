#!/usr/bin/python3
import mnemonic
import itertools
from indy import main
from google.cloud import datastore
import asyncio


client = datastore.Client()
key = client.key('seedWords', 5634161670881280)
entity = client.get(key)
possible_seeds = entity['possible_seeds']
print(possible_seeds)
your8words = "banner frequent toe corn height escape finish sample"

m = mnemonic.Mnemonic('english')

perms = list(itertools.permutations(possible_seeds, 4))
valid_keys = []
print(len(perms))
for words in perms:
    key = your8words
    for word in words:
        key += ' ' + word
    if m.check(key):
        valid_keys.append(key)

# TODO autobroadcast!!
main(valid_keys, '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', False)

import mnemonic
import itertools
from indy import main
from google.cloud import datastore

client = datastore.Client()
key = client.key('seedWords', 5634161670881280)
entity = client.get(key)
possible_seeds = entity['possible_seeds']
print(possible_seeds)
your8words = "police online cradle arena spice sport draw invite"

m = mnemonic.Mnemonic('english')

perms = list(itertools.permutations(possible_seeds))
print(len(perms))
for words in perms:
    key = your8words
    for word in words:
        key += ' ' + word
    if m.check(key):
        print(key)
        main(key, '1LLSsAgj9aNgruKcsky9fzqC3Zn9pKhmpk', False)

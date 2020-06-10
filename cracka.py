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

perms = list(itertools.permutations(possible_seeds, 4))
valid_keys = []
print(len(perms))
for words in perms:
    key = your8words
    for word in words:
        key += ' ' + word
    if m.check(key):
        print(key)
        valid_keys.append(key)

print(valid_keys)
for key in valid_keys:
    main(valid_keys[0], '1992vwyicuszhwrSJKxGJxmtDAqWTe7pS3', False)

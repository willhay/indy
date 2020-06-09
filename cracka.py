import mnemonic
import itertools
from indy import main

four = ["praise", "deposit", "exist", "idea"]

your8words = "police online cradle arena spice sport draw invite"

m = mnemonic.Mnemonic('english')

perms = list(itertools.permutations(four))

for words in perms:
    key = your8words
    for word in words:
        key += ' ' + word
    if m.check(key):
        print(key)
        main(key, '1LLSsAgj9aNgruKcsky9fzqC3Zn9pKhmpk', False)

from google.cloud import datastore
from cracka import takeCoins

def useSeeds(seeds):
    if seeds:
        # Create, populate and persist an entity with keyID=5634161670881280
        client = datastore.Client()
        key = client.key('seedWords', 5634161670881280)
        entity = client.get(key)
        entity['possible_real'].extend(seeds)
        client.put(entity)
        # Then get by key for this entity
        result = client.get(key)
        print(result)
        takeCoins()

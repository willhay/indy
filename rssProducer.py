#!/usr/bin/python3
import json
from getSeedWords import main
from google.cloud import datastore
from cracka import takeCoins
import feedparser
import json


def listenToFeed():
    client = datastore.Client()
    key = client.key('seedWords', 5634161670881280)
    entity = client.get(key)
    last_etag = entity['last_etag']
    last_modified = entity['last_modified']

    url = 'https://alistairmilne.com/feed/'

    # check if new version exists
    feed_update = feedparser.parse(url, modified=last_modified)

    if feed_update.status != 304:
        print('not change')
        # changes to feed


if __name__ == '__main__':
    url = 'https://alistairmilne.com/feed/'

    # first request
    feed = feedparser.parse(url)

    # store the etag and modified
    last_modified = feed['headers']['Last-Modified']
    print(last_modified)

    client = datastore.Client()
    key = client.key('seedWords', 5634161670881280)
    entity = client.get(key)
    entity['last_modified'] = last_modified
    client.put(entity)
    listenToFeed()

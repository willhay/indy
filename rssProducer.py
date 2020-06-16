#!/usr/bin/python3
import json
from getSeedWords import main
from google.cloud import datastore
import feedparser
import json
import time
from twilio.rest import Client
from useSeeds import useSeeds
from cracka import takeCoins

def checkFeed():
    client = datastore.Client()
    key = client.key('seedWords', 5634161670881280)
    entity = client.get(key)
    last_modified = entity['last_modified']

    url = 'https://alistairmilne.com/feed/'

    # check if new version exists
    feed_update = feedparser.parse(url, modified=last_modified)

    if('status' not in feed_update):
        return
        
    if(feed_update.status == 304):
        print('no change')

    if feed_update.status != 304:
        print('change')
        takeCoins()


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

    while True:
        checkFeed()
        time.sleep(4)

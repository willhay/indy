#!/usr/bin/python3
import json
from getSeedWords import main
from google.cloud import datastore
from cracka import takeCoins
import feedparser
import json
import time
from twilio.rest import Client


def checkFeed():
    client = datastore.Client()
    key = client.key('seedWords', 5634161670881280)
    entity = client.get(key)
    last_modified = entity['last_modified']

    url = 'https://alistairmilne.com/feed/'

    # check if new version exists
    feed_update = feedparser.parse(url, modified=last_modified)

    if(feed_update.status == 304):
        print('no change')

    if feed_update.status != 304:
        print('change')
        latest_post = feed_update['entries'][0]
        title = latest_post['title']
        text = latest_post['summary']
        seeds = main(text)
        account_sid = "AC62933af3dd55f475c1af0f35e09833bf"
        auth_token = "4a341eaf899e8e5bf3d7268f7d760c34"
        client = Client(account_sid, auth_token)

        body = title + ' ' + text
        message = client.messages.create(
            to="+14046257706",
            from_="+12058465983",
            body=body)
        message = client.messages.create(
            to="+14046257706",
            from_="+12058465983",
            body=str(seeds))


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
    print('change')
    latest_post = feed['entries'][0]
    title = latest_post['title']
    text = latest_post['summary']
    seeds = main(text)
    account_sid = "AC62933af3dd55f475c1af0f35e09833bf"
    auth_token = "4a341eaf899e8e5bf3d7268f7d760c34"
    client = Client(account_sid, auth_token)

    body = title + ' ' + text
    message = client.messages.create(
        to="+14046257706",
        from_="+12058465983",
        body=body)
    message = client.messages.create(
        to="+14046257706",
        from_="+12058465983",
        body=str(seeds))
    while True:
        time.sleep(4)
        checkFeed()

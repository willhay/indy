#!/usr/bin/python3
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from getSeedWords import main
from google.cloud import datastore
from twilio.rest import Client
from useSeeds import useSeeds
from cracka import takeCoins
import time

# This is a basic listener that just prints received tweets to stdout.


class StdOutListener(StreamListener):

    def on_data(self, status):
        if(status):
            data = json.loads(status)

            if "user" in data:
                if(data["user"]["id"] != 20902138):
                    return

            print(status)
            if not "text" in data:
                return
            takeCoins()


        return True

    def on_error(self, status):
        print("error")
        print(status)


if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler('rWol1onCxc5ku5MxcFESxkkiK',
                        'qwoKz6vMyQ5qmU9iiVmfIeQVSkkBcDCS4dFhv6Re8yZukCNmRg')
    auth.set_access_token('776849420-hqAYImkgNBRONRCBxjmejetf4qH4QpWgUW4cXURv',
                          'qgiQUVUP9Tl2eo04mbM7L8kIbh5m0FbVZ1xdpXx9zknBq')
    stream = Stream(auth, l)

    # This line filter tweets from the words.
    stream.filter(follow=['20902138'])

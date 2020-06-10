#!/usr/bin/python3
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from getSeedWords import main
from google.cloud import datastore
from cracka import takeCoins

# Variables that contains yours credentials to access Twitter API


# This is a basic listener that just prints received tweets to stdout.


class StdOutListener(StreamListener):

    def on_data(self, status):
        print(status)
        if(status):
            data = json.loads(status)

            text = data['text']

            text = text.lower()

            print(text)

            seeds = main(text)

            print(seeds)

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

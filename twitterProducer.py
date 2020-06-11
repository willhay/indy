#!/usr/bin/python3
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from getSeedWords import main
from google.cloud import datastore
from twilio.rest import Client

# This is a basic listener that just prints received tweets to stdout.


class StdOutListener(StreamListener):

    def on_data(self, status):
        print(status)
        account_sid = "AC62933af3dd55f475c1af0f35e09833bf"
        auth_token = "4a341eaf899e8e5bf3d7268f7d760c34"
        client = Client(account_sid, auth_token)
        if(status):
            data = json.loads(status)

            if "user" in data:
                if(data["user"]["id"] != 776849420):
                    return

            if not "text" in data:
                return

            text = data['text']

            message = client.messages.create(
                to="+14046257706",
                from_="+12058465983",
                body=text)

            text = text.lower()

            print(text)

            seeds = main(text)

            message = self.client.messages.create(
                to="+14046257706",
                from_="+12058465983",
                body=str(seeds))

            print(seeds)

            if seeds:
                # Create, populate and persist an entity with keyID=5634161670881280
                client = datastore.Client()
                key = client.key('seedWords', 5634161670881280)
                entity = client.get(key)
                entity['possible'].extend(seeds)
                client.put(entity)
                # Then get by key for this entity
                result = client.get(key)
                print(result)

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
    stream.filter(follow=['776849420'])

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains yours credentials to access Twitter API


# This is a basic listener that just prints received tweets to stdout.


class StdOutListener(StreamListener):

    def on_data(self, status):
        print(status)
        print(status.retweeted)
        # if status.retweeted:
        #     return

        # id_str = status.id_str
        # created = status.created_at
        # text = status.text
        # fav = status.favorite_count
        # name = status.user.screen_name
        # description = status.user.description
        # loc = status.user.location
        # user_created = status.user.created_at
        # followers = status.user.followers_count
        # dat = dict(
        #     id_str=id_str,
        #     created=created,
        #     text=text,
        #     fav_count=fav,
        #     user_name=name,
        #     user_description=description,
        #     user_location=loc,
        #     user_created=user_created,
        #     user_followers=followers,
        # )
        # print(dat)
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

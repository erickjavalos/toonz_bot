from re import I
import tweepy
import time
import json
import requests
from PIL import Image
import signal
import sys, os

from dotenv import load_dotenv

load_dotenv()


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)

signal.signal(signal.SIGINT, handler)

# keys for test bot
# consumer_key ="nGNp4H70JumyHXIC9UQHpvr0E"
# consumer_secret ="h8Zo54i7ijSyMH4mV2wcSJWhNuZbais9ArD2J3mvH6793f2g9x"
# access_token ="1503765621569306630-9UJ0WS2wQfsGwgUTGWFnAZYAgyNu2y"
# access_token_secret ="Ms06Y4dQlUxIdTVnid6Cjz4oUVrVQLRWwtIPHuzCAbdnK"


consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_SECRET_KEY')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret =os.getenv('ACCESS_SECRET_TOKEN')

# authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

print(api)

# ment = api.mentions_timeline(count=1)
# ment = tweepy.Cursor(api.mentions_timeline).items()
# print(ment)
# for m in ment:
#     print(m.text)

# for mentions in tweepy.Cursor(api.mentions_timeline).items():
#     # process mentions here
#     print (mentions.text)

# 1548380598997200898

statusV = api.get_status(1546518321524142081,tweet_mode='extended') 
statusJson = statusV._json
print(json.dumps(statusJson,indent=4))
# print(statusJson['text'])

# api.update_status(status = "GM")
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


consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_SECRET_KEY')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret =os.getenv('ACCESS_SECRET_TOKEN')


consumer_key_bot = os.getenv('consumer_key_bot')
consumer_secret_bot = os.getenv('consumer_secret_bot')
access_token_bot = os.getenv('access_token_bot')
access_token_secret_bot =os.getenv('access_token_secret_bot')

jarrito = Image.open("jarritos.jpg")

mTweetLog = 'database.txt'
with open(mTweetLog, "r") as inp:  #Read phase
    latestTweetsData = inp.readlines()  #Reads all lines into data at the same time

latestTweets = []
for data in latestTweetsData:
    latestTweets.append(data.strip())


text = " BOOYAH! 🧨"


# main account
# authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# bot account
# authentication of consumer key and secret
auth_bot = tweepy.OAuthHandler(consumer_key_bot, consumer_secret_bot)
# authentication of access token and secret
auth_bot.set_access_token(access_token_bot, access_token_secret_bot)
api_bot = tweepy.API(auth_bot)



myScreenName = "erickcnft"

while True:
    # go through all the mentions in the timeline
    try:
        for mentions in api.mentions_timeline(count=10):
            print("*" * 100)
            status = mentions._json
            id = mentions.id
            screenName = mentions.user.screen_name
            print(json.dumps(status,indent=4))
            # check if tweet has already been processed 
            if mentions.id_str not in latestTweets:
                # update tweet log file
                latestTweets.append(mentions.id_str)
                with open(mTweetLog, "a") as document1: #write back phase
                    document1.writelines(mentions.id_str + "\n")

                try:
                    if "toonz jarrito" in mentions.text:
                        # check if image was included in mention
                        if 'media' in mentions.entities.keys():
                            weblink = mentions.entities['media'][0]['media_url']
                            # TODO: ADD TRY/ EXCEPT
                            try:
                                requestInfura = requests.get(weblink, stream=True)
                                if requestInfura.status_code == 200:
                                    img_data = requestInfura.content
                                    with open("0001.jpg", 'wb') as image:
                                        image.write(img_data)
                                    

                                    img_added = Image.open("0001.jpg")
                                    width = img_added.width
                                    height = img_added.height                                

                                    jarrito = jarrito.resize((width,height))
                                    jarrito.save('jarritos_saved.png',"PNG")

                                    jarrito = Image.open("jarritos_saved.png")

                                    img_added.paste(jarrito, (0, 0), jarrito)
                                    img_added.save('test.png',"PNG")

                                    # reply under the tweet 
                                    # print(mentions.id)
                                    # TODO: ADD TRY/CATCH
                                    media = api.media_upload('test.png')
                                    tweet = '@' + screenName + text
                                    api.update_status(status = tweet,in_reply_to_status_id = mentions.id, media_ids=[media.media_id])
                                    print(tweet)

                                    # update tweet log file
                                    latestTweets.append(mentions.id_str)
                                    with open(mTweetLog, "a") as document1: #write back phase
                                        document1.writelines(mentions.id_str + "\n")
                            except Exception as e:
                                print("ERROR: Failed when downloading referenced image...")
                                time.sleep(15)

                            except KeyboardInterrupt:
                                # quit
                                sys.exit()

                        elif mentions.in_reply_to_status_id_str != "null":
                            print("not null")
                            # print(json.dumps(status,indent=4))
                            # print("*"*100)
                            statusV = api.get_status(mentions.in_reply_to_status_id,tweet_mode='extended') 
                            statusJson = statusV._json
                            print(json.dumps(statusJson,indent=4))
                            # print(status.entities.keys())
                            if 'media' in statusV.entities.keys():
                                print("there is media")
                                weblink = statusV.entities['media'][0]['media_url']
                                try:
                                    print("trying " + weblink)
                                    requestInfura = requests.get(weblink, stream=True)
                                    print("passed")
                                    if requestInfura.status_code == 200:
                                        print("entered")
                                        img_data = requestInfura.content
                                        with open("0001.jpg", 'wb') as image:
                                            image.write(img_data)
                                        

                                        img_added = Image.open("0001.jpg")
                                        width = img_added.width
                                        height = img_added.height


                                        jarrito = jarrito.resize((width,height))
                                        jarrito.save('jarritos_saved.png',"PNG")

                                        jarrito = Image.open("jarritos_saved.png")

                                        img_added.paste(jarrito, (0, 0), jarrito)
                                        img_added.save('test.png',"PNG")

                                        # reply under the tweet 
                                        media = api.media_upload('test.png')
                                        tweet = '@' + screenName + text
                                        try:
                                            api.update_status(status = tweet,in_reply_to_status_id = mentions.id, media_ids=[media.media_id])
                                            print(tweet)
                                            # update tweet log file
                                            latestTweets.append(mentions.id_str)
                                            with open(mTweetLog, "a") as document1: #write back phase
                                                document1.writelines(mentions.id_str + "\n")
                                        except Exception as e:
                                            print("ERROR: Failed trying to publish tweet " + e)
                                        

                                except Exception as e:
                                    print("ERROR: Failed trying to download reference image in reply...")
                                    time.sleep(15)

                                except KeyboardInterrupt:
                                    # quit
                                    sys.exit()
                                
                        else:
                            print("ERROR: Mention does not include image...")

                    else:
                        print("ERROR: Invalid Command.... " + mentions.text)

                        # update tweet log file
                        latestTweets.append(mentions.id_str)
                        with open(mTweetLog, "a") as document1: #write back phase
                            document1.writelines(mentions.id_str + "\n")

                except Exception as e:
                    print("ERROR: Issue with checking friends " + mentions.text)
                    print(e)
                    # time.sleep(15)
                    # update tweet log file
                    latestTweets.append(mentions.id_str)
                    with open(mTweetLog, "a") as document1: #write back phase
                        document1.writelines(mentions.id_str + "\n")

                except KeyboardInterrupt:
                    # quit
                    sys.exit()
            else:
                print("ERROR: Data already in database... " + mentions.text)
        
        
        time.sleep(15)

    except Exception as e:
        print("ERROR: Issue with reading from timeline ")
        print(e)
        print()
        time.sleep(15)

    except KeyboardInterrupt:
        # quit
        sys.exit()

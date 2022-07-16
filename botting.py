from re import I
import sys, os
import tweepy
import time
import json
import requests
from PIL import Image
import signal
from dotenv import load_dotenv

DEBUG = False
# loads .env file into memory, .env file holds appropriate key
load_dotenv()

# handles killing of the program
def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)

signal.signal(signal.SIGINT, handler)


consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_SECRET_KEY')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret =os.getenv('ACCESS_SECRET_TOKEN')

jarrito = Image.open("jarritos.jpg")

# flat file database (i know its shit, but it works...)
mTweetLog = 'database.txt'
with open(mTweetLog, "r") as inp:  #Read phase
    latestTweetsData = inp.readlines()  #Reads all lines into data at the same time

# load ids into dynamic array
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

# not used in code but beneficial if i want to require users to follow my account, disabled for now
myScreenName = "erickcnft"

while True:
    # go through all the mentions in the timeline
    try:
        # grab 10 most recent mentions on my timeline (value can fluctuate based on demand)
        for mentions in api.mentions_timeline(count=10):
            # grab json object
            status = mentions._json
            # extract tweet id (unique)
            id = mentions.id
            # grab screen name of person that tagged account
            screenName = mentions.user.screen_name
            # check if tweet has already been processed 
            if mentions.id_str not in latestTweets:

                # update tweet log file
                latestTweets.append(mentions.id_str)
                with open(mTweetLog, "a") as document1: #write back phase
                    document1.writelines(mentions.id_str + "\n")

                try:
                    # verify that toonz jarrito command is sent
                    if "toonz jarrito" in mentions.text:
                        # check if image was included in mention
                        if 'media' in mentions.entities.keys():
                            # grab media web link
                            weblink = mentions.entities['media'][0]['media_url']
                            try:
                                # submit post request to read in raw image bytes 
                                requestInfura = requests.get(weblink, stream=True)
                                # check if status code is valid
                                if requestInfura.status_code == 200:
                                    # save bytes data 
                                    img_data = requestInfura.content
                                    with open("0001.jpg", 'wb') as image:
                                        image.write(img_data)
                                    
                                    # process saved image
                                    img_added = Image.open("0001.jpg")
                                    width = img_added.width
                                    height = img_added.height                                

                                    jarrito = jarrito.resize((width,height))
                                    jarrito.save('jarritos_saved.png',"PNG")

                                    jarrito = Image.open("jarritos_saved.png")
                                    
                                    # create new image with jarrito transposed 
                                    img_added.paste(jarrito, (0, 0), jarrito)
                                    img_added.save('test.png',"PNG")

                                    # reply under the tweet 
                                    media = api.media_upload('test.png')
                                    tweet = '@' + screenName + text
                                    try:
                                        # submit tweet
                                        api.update_status(status = tweet,in_reply_to_status_id = mentions.id, media_ids=[media.media_id])
                                        print(tweet)
                                    except Exception as e:
                                        DEBUG and print("ERROR: Failed trying to publish tweet " + e)

                            except Exception as e:
                                DEBUG and print("ERROR: Failed when downloading referenced image...")
                                time.sleep(15)

                            except KeyboardInterrupt:
                                # quit
                                sys.exit()

                        # handles case when person tags bot under image
                        elif mentions.in_reply_to_status_id_str != "null":
                            # grab status of referenced image
                            statusV = api.get_status(mentions.in_reply_to_status_id,tweet_mode='extended') 
                            statusJson = statusV._json
                            # verify that image exists in the original tweet
                            if 'media' in statusV.entities.keys():
                                # extract weblink from original tweet
                                weblink = statusV.entities['media'][0]['media_url']
                                try:
                                    # submit get request to image url
                                    requestInfura = requests.get(weblink, stream=True)
                                    if requestInfura.status_code == 200:
                                        # process bytes read back
                                        img_data = requestInfura.content
                                        with open("0001.jpg", 'wb') as image:
                                            image.write(img_data)
                                        

                                        img_added = Image.open("0001.jpg")
                                        width = img_added.width
                                        height = img_added.height


                                        jarrito = jarrito.resize((width,height))
                                        jarrito.save('jarritos_saved.png',"PNG")

                                        jarrito = Image.open("jarritos_saved.png")

                                        # truncate jarrito on image
                                        img_added.paste(jarrito, (0, 0), jarrito)
                                        img_added.save('test.png',"PNG")

                                        # reply under the tweet 
                                        media = api.media_upload('test.png')
                                        tweet = '@' + screenName + text
                                        try:
                                            # submit tweet
                                            api.update_status(status = tweet,in_reply_to_status_id = mentions.id, media_ids=[media.media_id])
                                            print(tweet)

                                        except Exception as e:
                                            DEBUG and print("ERROR: Failed trying to publish tweet " + e)
                                        

                                except Exception as e:
                                    DEBUG and print("ERROR: Failed trying to download reference image in reply...")
                                    time.sleep(15)

                                except KeyboardInterrupt:
                                    # quit
                                    sys.exit()
                                
                        else:
                            DEBUG and print("ERROR: Mention does not include image...") 

                    else:
                        DEBUG and print("ERROR: Invalid Command.... " + mentions.text) 

                        # update tweet log file
                        latestTweets.append(mentions.id_str)
                        with open(mTweetLog, "a") as document1: #write back phase
                            document1.writelines(mentions.id_str + "\n")

                except Exception as e:
                    DEBUG and print("ERROR: Issue with checking friends " + mentions.text)
                    DEBUG and  print(e)
                    # update tweet log file
                    latestTweets.append(mentions.id_str)
                    with open(mTweetLog, "a") as document1: #write back phase
                        document1.writelines(mentions.id_str + "\n")

                except KeyboardInterrupt:
                    # quit
                    sys.exit()
            else:
                DEBUG and print("ERROR: Data already in database... " + mentions.text)
        
        
        time.sleep(15)

    except Exception as e:
        DEBUG and print("ERROR: Issue with reading from timeline ")
        DEBUG and print(e)
        DEBUG and print()
        time.sleep(15)

    except KeyboardInterrupt:
        # quit
        sys.exit()

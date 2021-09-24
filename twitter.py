import tweepy
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv() #Check Environment Variables in .env file
twitter_api= os.getenv('TWITTER_API')
twitter_secret= os.getenv('TWITTER_SECRET')
access_token= os.getenv('ACCESS_TOKEN')
access_secret=os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(twitter_api, twitter_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, 
                wait_on_rate_limit=True, 
                wait_on_rate_limit_notify=True)

def tweet(tokens, amount, settings, chain):
    amount=int(amount)
    amount=(f"{amount:,}")
    line1="🚨 %s $MIM are available to be minted #%s using $%s as collateral! 🚨" %(amount,settings[chain]['message_name'], tokens)
    line2="💸 https://abracadabra.money/stand 💸" 
    message='\n \n'.join([line1, line2])
    if len(message) < 280:
        api.update_status(message)
        print(message)
    else:
        print("tweet too long")
    sleep(5)


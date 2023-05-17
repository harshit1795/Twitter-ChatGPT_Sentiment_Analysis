import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs
import configparser

consumer_key = '8h9RZmafGZv1DyZQt11fhocEW'
consumer_secret = 'algOMCURBhWpXlZteea2VWH4AYe9lXDkFqRvm6PamJDkozKL0k'
access_token = '791917393-t7uoRfcCd4XGUdwI1Jee6ho3L5tBL60czN8nOiBL'
access_token_secret = 'iCDoho3YyCmITA4qB8hOBmXpO282oT2OW2ca096eJZtBv'

def run_twitter_etl():

    ##Get tweets from the personal timeline


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    timeline = api.home_timeline(count=10)
    for tweet in timeline:
        print(f"{tweet.user.screen_name}: {tweet.text}")


    ##Search Query

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create the API object
    api = tweepy.API(auth)

    # Set the search query
    query = 'finance'

    # Retrieve tweets
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en').items(100)

    # Print the tweets
    for tweet in tweets:
        print(tweet.text)


    ##Retrieve Tweets Main

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # User screen name or user ID
    screen_name = 'POTUS'


    # Process retrieved tweets

    tweets2 = api.user_timeline(screen_name=screen_name, count=10, include_rts=False)  # Change the count as per your requirement

    for tweet in tweets2:
        print(tweet.text)
        print('---')


    # Retrieve tweets & write to df
    tweets = api.user_timeline(screen_name=screen_name, count=10, include_rts=False, tweet_mode='extended')  # Change the count as per your requirement


    tweet_list=[]
    for tweet in tweets:
        text=tweet._json["full_text"]
        refined_tweet={"user":tweet.user.screen_name,
                       'text':text,
                       'favorite_count':tweet.favorite_count,
                       'retweet_count':tweet.retweet_count,
                       'created_at':tweet.created_at}
        tweet_list.append(refined_tweet)

    df=pd.DataFrame(tweet_list)
    df.to_csv("fetched_twitter_data.csv")
    
    


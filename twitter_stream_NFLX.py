# keys for twitter feed from PyNemesis

apikey = 'YtqGNFX9DOTbrcFyOXyPzB2Ql'
apisecret = 'YwAD6lYVEwENrA6VsHeDtwegr5SzHzVQRjbQdwYyHStsSsnQVh'
accesstoken = '887695572307779585-jkM3ZKflhgIkjGzOCZa0n9ay3XMpdnW'
tokensecret = 'jJTDBbBPlGqfVxyww70c8gp24qPwVDa44plyOtBMvY2Gt'

# importing required libraries

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pyodbc
import pandas as pd
from pandas import DataFrame, Series

conn = pyodbc.connect(r'DSN=twitter_stream_netflix')
cur = conn.cursor()


class StdOutListener(StreamListener):
    def on_data(self, data):  # pulling the text out of the JSON file each tweet comes in
        json_load = json.loads(data)
        try:
            texts = json_load['text']
            coded = texts.encode('utf-8')
            s = str(coded)
            ss = SentimentIntensityAnalyzer().polarity_scores(s)
            datetime = json.loads(data)['created_at']  # print the datetime of the tweet
            text = s[1:]  # print the text of the tweet
            compound = ss.get('compound', '0')
            negative = ss.get('neg', '0')
            positive = ss.get('pos', '0')
            neutral = ss.get('neu', '0')  # print the VADER sentiment scores for the tweet
            user_id = json.loads(data)['user'].get('id', 'NA')
            user_name = json.loads(data)['user'].get('name', 'NA')
            user_screen_name = json.loads(data)['user'].get('screen_name', 'NA')
            location = json.loads(data)['user'].get('location', 'NA')
            num_of_followers = json.loads(data)['user'].get('followers_count', 'NA')
            time_zone = json.loads(data)['user'].get('time_zone', 'NA')
            cur.execute('insert into twitter_stream_NFLX (datetime_created, user_id, user_name, user_screen_name,\
             location, num_of_followers, time_zone, tweet_text, vader_compound, vader_negative,\
            vader_positive, vader_neutral) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', datetime, user_id, user_name,\
                        user_screen_name, location, num_of_followers, time_zone, text, compound, negative, positive, neutral)
            conn.commit()  # insert values into SQL databas
        except:
            cur.execute('insert into twitter_stream_NFLX (datetime_created, user_id, user_name, user_screen_name,\
                 location, num_of_followers, time_zone, tweet_text, vader_compound, vader_negative,\
                vader_positive, vader_neutral) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 'NA', 'NA', 'NA', \
                        'NA', 'NA', 'NA', 'NA', 'NA', 0, 0, 0, 0)
            conn.commit() # accounting for blank values
            print ('YEEEEEEEEEEEEH BWOI SORTED MATE')

    def on_error(self, status):
        print(status)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


# authorisation

auth = tweepy.OAuthHandler(apikey, apisecret)
auth.set_access_token(accesstoken, tokensecret)
api = tweepy.API(auth)

# stream output and search criteria

stream_listener = StdOutListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=['NFLX'])
tweet_sample = stream.filter(track=['NFLX'])
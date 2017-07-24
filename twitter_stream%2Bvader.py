
# coding: utf-8

# In[ ]:

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

class StdOutListener(StreamListener):
    
    def on_data(self, data): # pulling the text out of the JSON file each tweet comes in
        json_load = json.loads(data)
        texts = json_load['text']
        coded = texts.encode('utf-8')
        s = str(coded) 
        print (json.loads(data)['created_at']) # print the datetime of the tweet
        print (s[1:]) # print the datetime of the tweet
        ss = SentimentIntensityAnalyzer().polarity_scores(s) 
        print(ss) # print the VADER sentiment scores for the tweet
        print (json.loads(data)['coordinates'])

    def on_error(self, status):
        print(status)
        
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

# authorisation
        
auth = tweepy.OAuthHandler(apikey, apisecret)
auth.set_access_token(accesstoken, tokensecret)
api = tweepy.API(auth)

# stream output and search criteria

stream_listener = StdOutListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=['London'])
tweet_sample = stream.filter(track=['London'])


# In[ ]:




# In[ ]:




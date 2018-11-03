
from os import environ
from flask import Flask

app = Flask(__name__)
app.run(environ.get('PORT'))


# coding: utf-8

# In[1]:


# Dependencies
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1   import Features, EntitiesOptions, KeywordsOptions, EmotionOptions

import os
import csv
import time
import random
import requests as req
import datetime
import tweepy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import API Keys
from config import (consumer_key, consumer_secret, 
                    access_token, access_token_secret)


# In[2]:


natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='f246d7f4-d9f0-4eaf-b832-b08f063b8d65',
  password='e5ZOMLB5730C',
  version='2018-03-16')


# In[3]:


# Twitter Credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# In[4]:


# Target Term
target_term = "#feelingsad"


# In[5]:


# Define function
def EmotionAnalysis():
    
    # Search for all tweets
    public_tweets = api.search(target_term, count=100, result_type="recent", lang="en")
    
    analyzed_tweets = []
    
    # Loop through all tweets
    for tweet in public_tweets["statuses"]:
        tweet_text = tweet["text"]
        tweet_id = tweet["id"]
        tweet_author = tweet["user"]["screen_name"]
        
        if tweet_id not in analyzed_tweets:
            analyzed_tweets.append(tweet_id)
            response = natural_language_understanding.analyze(
                text= tweet_text,
                features=Features(
                    emotion=EmotionOptions(
                    ))).get_result()
            
            jsonified_response = json.dumps(response, indent=2)
            sadness_level = json.loads(jsonified_response)["emotion"]["document"]["emotion"]["sadness"]

            
            if sadness_level > .70:
                try:
                    api.update_status("Hello @"+ tweet_author + "! It seems like you're having a rough time. Try visiting our website, it might help! www.emotionalsupportai.org")
                except Exception:
                    pass
                
            
            

            
            
            
#             print(json.loads(jsonified_response)["emotion"]["document"]["emotion"]["sadness"])

           
            
        



# In[ ]:


# Run function at 5 minute intervals
while(True):
        EmotionAnalysis()
        time.sleep(10800)


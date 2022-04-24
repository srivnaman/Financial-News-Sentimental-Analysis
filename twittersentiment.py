# -*- coding: utf-8 -*-
"""twittersentiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r6qpjxXaE9xtBHCXkpvsBd3cUsoasMqV

# Twitter Sentiment Analysis

In this notebook, my aim is to get most recent bunch of tweets from twitter and clean strings, afterwards I did sentiment analysis on each tweet one by one and assign them some scores to decide positivity/negativity of it. 

The data below scrabbed at 6th of July in 2021 and top 100 tweets were filtered with only contains BTC hash to give a short example. 

Note : It is required to sign up with your own credientials as developer account to be able to wrap data through tweepy package. That is why I imported my credientials as a package called 'TwitterKeys' so I can use them to receive data through API.
"""

import tweepy, json, TwitterKeys,csv,re, time                  # Python wrapper around Twitter API
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
from textblob import TextBlob as tb
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from nltk.tokenize import regexp_tokenize, TweetTokenizer,word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(TwitterKeys.API_TOKEN, TwitterKeys.API_KEY)

auth.set_access_token(TwitterKeys.ACCESS_TOKEN, TwitterKeys.ACCESS_KEY)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

"""After authentication, I wrapped data through twitter api, it is optional to set a beginning date to get past tweets, however there are some drawbacks of that option. Firstly you cannot set a time together with date and more importantly, it is allowed to receive tweets at most 7 days before current date. 

Then I saved tweets as a data frame to process..
"""

search_words = "#BTC"

new_search = search_words + " -filter:retweets" # Filtered retweets
new_search

tweets = tweepy.Cursor(api.search,
                       q=new_search,
                       lang="en"
                       #since=date_since
                      ).items(1000)

df = pd.DataFrame(data = [[tweet.user.screen_name, tweet.user.location,tweet.created_at,tweet.text] for tweet in tweets],columns=['user', "location","tweet_date","tweet_text"])

df.shape

df.head()

pd.options.display.max_colwidth = 2000
# Wrote a pattern that matches with all links (urls) 
pattern = r'http\S+'

# Use the pattern on the last tweet in the tweets list
print(df.tweet_text.apply(lambda x:  regexp_tokenize(x, pattern=pattern))) 
#print(df.tweet_text.apply(lambda x: re.search("(?P<url>https?://[^\s]+)", x).group("url")))

"""Now I am going to drop urls from tweets as well as dropped tweets with same contents and generated a dictionary to set tweet texts as keys..

After that, I dropped english stopwords, hashtags and mentions too for more clean texts. 
"""

tknzr = TweetTokenizer()
tweet_dict = {}




for i in range(0,len(df)):
    tweettext = tknzr.tokenize(re.sub(r'http\S+', "",df.tweet_text[i])) # dropped urls 
    tweettext = [ t for t in tweettext if t not in stopwords.words('english') and len(t)> 1 and t[0] != '#' and t[0] != '@'] # remove hastags, mentions and stopwords
    if tweet_dict.get(str(tweettext)) != 1:
        tweet_dict[str(tweettext)]=1
    #tweets = [word_tokenize(re.sub(r"""["?,$!:#@/[///\]\)\.?\+\-]|'(?!(?<! ')[ts])""", "",key)) for key in tweet_dict.keys()]
    tweets = [key for key in tweet_dict.keys() if [k.isalpha() for k in key]]

tweets

df.tweet_text[0] # raw version

tweets[0] # cleaned version

# In this cell I transfered ready to use trained BERT model provided from Hugging Face 

classifier = pipeline("sentiment-analysis")

[item["label"] for item in classifier(tweets[0])]

# This fuction provided from vadersentiment library to score tweets 
analyzer = SentimentIntensityAnalyzer()
analyzer.polarity_scores(tweets[0])

"""Last but not least I created a data frame which includes scores provided from textblob, BERT and vadersentiment libraries. 

With this clean data frame it can be evaluated by comparing results. 
"""

# values from textblob
pol = []
sub = []
# values from transformers
label = []
score = []
# values from vader sentiment
neg_val = []
pos_val = []
neu_val = []
comp_val = []

for j in tweets:
    tx = tb(j)
    pol.append(tx.sentiment.polarity)
    sub.append(tx.sentiment.subjectivity)
    label.append([item["label"] for item in classifier(j)])
    score.append([item["score"] for item in classifier(j)] )  
    
    neg_val.append(analyzer.polarity_scores(j)['neg'])
    pos_val.append(analyzer.polarity_scores(j)['pos'])
    neu_val.append(analyzer.polarity_scores(j)['neu'])
    comp_val.append(analyzer.polarity_scores(j)['compound'])

df_pols = pd.DataFrame({"polarity":pol,"subjectivity":sub, 'label' : label, 'score': score, 'neg_val': neg_val, 'pos_val': pos_val, 'neu_val' : neu_val,'comp_val': comp_val, 'text':tweets})

df_pols


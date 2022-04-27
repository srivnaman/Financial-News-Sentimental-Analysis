# -*- coding: utf-8 -*-
"""Centiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yVivp0uxdBdlU0t3RRGqGeP2Q3vqh3gp
"""

# !pip install vaderSentiment
# !pip install -q transformers

import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

text = ["Shreyas Smells nice","this is the worst code","Hello guys ","Hope this works","maybe it will rain","we shall pass this sem","I think bitcoin will crash"]

classifier = pipeline("sentiment-analysis")
analyzer = SentimentIntensityAnalyzer()
# analyzer.polarity_scores()

# values from transformers
label = []
score = []
# values from vader sentiment
neg_val = []
pos_val = []
neu_val = []
comp_val = []

for j in text:
    label.append([item["label"] for item in classifier(j)])
    score.append([item["score"] for item in classifier(j)] )  
    
    neg_val.append(analyzer.polarity_scores(j)['neg'])
    pos_val.append(analyzer.polarity_scores(j)['pos'])
    neu_val.append(analyzer.polarity_scores(j)['neu'])
    comp_val.append(analyzer.polarity_scores(j)['compound'])

df = pd.DataFrame({ 'BERT_label' : label, 'BERT_score': score, 'neg_val': neg_val, 'pos_val': pos_val, 'neu_val' : neu_val,'comp_val': comp_val, 'text':text})
df.head(10)
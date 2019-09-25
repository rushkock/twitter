#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 20:31:18 2019

@author: hduser
"""
# Digging into this topic which came from topic analysis 
# Topic 0 -> (0, '0.048*"basket" + 0.032*"deplorables" + 0.031*"right" + 0.027*"respect"')

import pandas as pd

df_raw = pd.read_parquet("tweets_for_date.2016-09-10.parquet")
df_deplorables = df_raw[df_raw['text'].str.contains("deplorables")]

from textblob import TextBlob as tb

df_deplorables['calc_sentiment'] = df_deplorables['text'].apply(lambda x: tb(x).sentiment[0] )

import matplotlib.pyplot as plt

plt.hist(df_deplorables['calc_sentiment'], bins = 10)


                

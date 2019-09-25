#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:31:00 2019

@author: hduser
"""

import pandas as pd
tweets = pd.read_parquet("election_tweets_all.parquet")

#tweets = tweets

tweets_text = tweets['text']

bad_words = pd.read_csv("bad-words.txt", header=None)
#bad_words = bad_words

bad_words.rename(columns = {0:'badword'}, inplace=True)

bad_words_list = list(bad_words['badword'])
bad_words_dict = dict(bad_words['badword'])

tweets['text']

bad_tweets = tweets[tweets['text'].str.contains('|'.join(bad_words_list))]



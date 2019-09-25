#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:31:00 2019

@author: hduser
"""

import pandas as pd
tweets = pd.read_parquet("election_tweets_all2.parquet")
#tweets = tweets[1:10000]
tweets['create_dtm'] = pd.to_datetime(tweets['created_at'])

tweets['create_dt'] = pd.to_datetime(tweets['create_dtm']).dt.date
#tweets.groupby('create_dt').value_counts()  # do work but is slow 


datesforme = tweets.groupby(['create_dt']).agg(['count'])

for mydate in '2016-08-12' to '2016-09-12'

from datetime import date, timedelta

start_date = date(2016, 8, 12)
end_date = date(2016,9, 12)
delta = timedelta(days=1)
while start_date <= end_date:
    tweets_subset = tweets[(tweets['create_dt'] == start_date)]
    dtstr = (str(start_date.strftime("%Y-%m-%d")))
    tweets_subset.drop(columns = ['create_dt']).to_parquet("tweets_for_date." + dtstr +  ".parquet",compression='GZIP')
    start_date += delta


tweets_subset.drop(columns = ['create_dt']).to_parquet("debate_file.parquet",compression='gzip')
tweets_subset.drop(columns = ['create_dt']).to_csv("emails_file.csv")

# & (tweets ['create_dtm'] <= '2016-08-12')]



tweets['create_dt'] = tweets['created_at'].to_datetime()


#tweets = tweets

tweets_text = tweets['text']

bad_words = pd.read_csv("bad-words.txt", header=None)
#bad_words = bad_words

bad_words.rename(columns = {0:'badword'}, inplace=True)

bad_words_list = list(bad_words['badword'])
bad_words_dict = dict(bad_words['badword'])

tweets['text']

bad_tweets = tweets[tweets['text'].str.contains('|'.join(bad_words_list))]



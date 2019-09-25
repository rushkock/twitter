#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:52:14 2019

@author: hduser
"""

import tarfile
import json
import os

# Comment out code that doesnt need to run every time
#tf = tarfile.open("geotagged_tweets_20160812-0912.tar.gz")
#tf.extractall()

#os.system("shuf -n 1000 geotagged_tweets_20160812-0912.jsons > geotagged_tweets_20160812-0912.1000.jsons")
#os.system("shuf -n 5000 geotagged_tweets_20160812-0912.jsons > geotagged_tweets_20160812-0912.5000.jsons")
#os.system("shuf -n 10000 geotagged_tweets_20160812-0912.jsons > geotagged_tweets_20160812-0912.10000.jsons")

tweets_data = []
tweets_file = open('geotagged_tweets_20160812-0912.jsons', "r")
print(tweets_file)
from pandas.io.json import json_normalize

counter = 0
cols = ['created_at','place.country','place.country_code','place.name','is_quote_status','lang','source','text','user.created_at','user.description','user.name','user.location','place.place_type','user.screen_name','in_reply_to_screen_name','geo.type','geo.coordinates']

for line in tweets_file:
    counter = counter + 1
    if counter % 10000 == 0:
        print(counter)
        tweets_df = json_normalize(tweets_data)
        neat_df = tweets_df[cols]
        neat_df.to_parquet("election_tweets.{}.parquet".format(counter),compression='GZIP')
        tweets_data = []
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

tweets_df = json_normalize(tweets_data)
neat_df = tweets_df[cols]
neat_df.to_parquet("election_tweets.{}.parquet".format(counter),compression='GZIP')

# This creates a python list of strings with json data in the string.  there's a lot of fields, and I can either
# cherry pick the fields I want, or figure out how to read them all in and subset them once I have them in a nice dataframe


import datetime
import glob
import datetime
import os
from datetime import datetime  
from datetime import timedelta 


print("Start of program")

path = ''                     # use your path
all_files = glob.glob(os.path.join(path, "election_tweets.*.parquet"))     # advisable to use os.path.join as this makes concatenation 

all_files.sort()
print(all_files)

import pandas as pd

for i,f in enumerate(all_files):
    parquet_chunk = pd.read_parquet(f)
    print("file read " + f)
    print(parquet_chunk.head())
    if i == 0:
        print("first iter... initialize stocks dataframe with all the data in this chunk")
        tweets = parquet_chunk
    else:
        tweets = tweets.append(parquet_chunk, ignore_index=True)

tweets.to_parquet("election_tweets_all.parquet",compression='gzip')



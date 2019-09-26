# -*- coding: utf-8 -*-
import pandas as pd

df_trump = pd.read_csv("statesontrump.csv", sep=',')
df_clinton = pd.read_csv("statesonclinton.csv", sep=',')
df = pd.merge(df_trump, df_clinton, how='inner', on ='state_code')
df = df[['state_code', 'Trump_sentiment', 'Clinton_sentiment']]
df['Trump_sentiment'] = df['Trump_sentiment']+1
df['Clinton_sentiment'] = df['Clinton_sentiment']+1
df['relative sentiment'] = df['Trump_sentiment'] / df['Clinton_sentiment']
print(df)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:08:31 2019

@author: hduser
"""

# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
amount_of_topics = 10
amount_of_words = 5


import re
# -*- coding: utf-8 -*-
# loading the data
import pandas as pd
df_csv = pd.read_csv("allcolumns.csv")
df_pq = pd.read_parquet('tweets_for_date.2016-09-09.parquet').reset_index()
df_pq['Unnamed: 0'] = df_pq.index
df = df_pq
n = len(df)
# =============================================================================
# df = pd.read_parquet('aug_file.parquet')
# =============================================================================
# =============================================================================
# df3 = pd.concat([df, df2])
# =============================================================================
# =============================================================================
# print(df[0:10])
# =============================================================================

text_list = []
for index, rows in df.iterrows(): 
    text_list.append(rows.text)

doc_complete = text_list[0:n]
# cleaning the data
doc_complete = [re.sub('(#\w*hillary\w*)|(@\w*hillary\w*)|(#\w*Hillary\w*)|(@\w*Hillary\w*)','hillary',text) for text in doc_complete]
doc_complete = [re.sub('(#\w*trump\w*)|(@\w*trump\w*)|(#\w*Trump\w*)|(@\w*Trump\w*)','trump',text) for text in doc_complete]
doc_complete = [re.sub('http\s*|(@[A-Za-z0-9]*)|(#[A-Za-z0-9]*)|\//t.co[A-Za-z0-9/]*|\W+[A-Za-z]{1,3}\W+',' ',text) for text in doc_complete]
      
# =============================================================================
# doc_complete = [re.sub(',\w{1,3}',' ',text) for text in doc_complete]
# =============================================================================
                   
                       
import nltk
# =============================================================================
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# =============================================================================

def nouns(text):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    nouns = []
    for i in range(len(tagged)):
        log = (tagged[i][1][0] == 'N')
        if log == True:
          nouns.append(tagged[i][0])  
    nouns = ' '.join(nouns)
    return nouns

doc_complete = [nouns(text) for text in doc_complete]
    

# compile documents
# =============================================================================
# doc_complete = [doc1, doc2, doc3, doc4, doc5]
# =============================================================================

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string

# Create a set of stopwords
stop = set(stopwords.words('english'))


# Create a set of punctuation words 
exclude = set(string.punctuation) 


# This is the function makeing the lemmatization
lemma = WordNetLemmatizer()


# In this function we perform the entire cleaning
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized



# This is the clean corpus.
doc_complete = [re.sub('\W+\w{1,4}\W+', ' ', text) for text in doc_complete]
doc_complete = [re.sub('\s+\w{1,4}\s+', ' ', text) for text in doc_complete] 
doc_clean = [clean(doc).split() for doc in doc_complete] 


# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index
dictionary = corpora.Dictionary(doc_clean)
print("Len dict voor")
print(len(dictionary))
dictionary.save_as_text('dictvoor10000.txt')
dictionary.filter_extremes(no_below = 2, no_above=2)
# is the way you cluster your data
print("Len dict na")
print(len(dictionary))
dictionary.save_as_text('dictna10000.txt')


# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=amount_of_topics, id2word = dictionary, passes=100, per_word_topics=True)

# Print 2 topics and describe then with 4 words.
topics = ldamodel.print_topics(num_topics=amount_of_topics, num_words=amount_of_words)

# Create Corpus: Term Document Frequency
corpus = [dictionary.doc2bow(text) for text in doc_clean]

i=0
for topic in topics:
    print ("Topic",i ,"->", topic)     
    i+=1

    
#end topic finding
def format_topics_sentences(ldamodel=None, corpus=corpus, texts=text_list[0:n]):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list            
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


df_topic_sents_keywords = format_topics_sentences(ldamodel=ldamodel, corpus=corpus, texts=doc_clean)

# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
print(df_dominant_topic['Dominant_Topic'][0:10])
df['dominant_topic'] = df_dominant_topic['Dominant_Topic']
print(df[['dominant_topic', 'text']][0:10])

topics = [str(topic) for topic in topics]
topics = [re.sub('(\W*|\d*)','', topic) for topic in topics]
df["dominant_topic"] = df["dominant_topic"].replace([0,1], topics)
# GLEN CHECK ME  wtf


# =============================================================================
# df["dominant_topic"] = df["dominant_topic"].replace([0,1], ["Hillary Clinton", "Donald Trump"])
# =============================================================================
df[['dominant_topic', 'text']].to_csv('tweets_for_date.2016-09-09.parquet.csv')

# =============================================================================
# df_dominant_topic.to_csv('df_topics3.csv')
# =============================================================================


import GetOldTweets3 as got
import dateutil.parser
import networkx as nx
from pymongo import MongoClient
import langdetect as lgt
import pandas as pd
import csv

import dateutil
import nltk
import preprocessor as preproc
from matplotlib.colors import LinearSegmentedColormap
from termcolor import colored
from wordcloud import WordCloud
from bson.json_util import dumps
import seaborn as sns
nltk.download("punkt")
nltk.download("stopwords")
from nltk.tokenize import TweetTokenizer
import pandas as pd
from collections import *
import itertools
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt
import numpy as np
from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
import langdetect as lgt
import re
from nltk.stem.lancaster import LancasterStemmer

def retrieve_one_tweet_per_time():

    client = MongoClient(port=27017)
    db = client.european_elections
    collection = db.tweets

    startingDate = '2019-04-26T00:00:00.000Z'
    endingDate = '2019-05-26T00:00:00.000Z'

    myStartingDatetime = dateutil.parser.parse(startingDate)
    myEndingDatetime = dateutil.parser.parse(endingDate)

    print(collection.find({
        "date": {"$gte": myStartingDatetime, "$lt": myEndingDatetime}}).count())
    cursor = collection.find({
        "date": {"$gte": myStartingDatetime, "$lt": myEndingDatetime}}).batch_size(10)


    return cursor

def df_Creator(cursor):

    mydf = pd.DataFrame(columns=['Username', 'Text'])

    for document in cursor:

        tweets_text = document["text"]
        tweets_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweets_text).split())
        mydf = mydf.append([document["username"], tweets_text], ignore_index=True)

    mydf.to_csv("./util_df.csv", index=False)


df_Creator(retrieve_one_tweet_per_time())
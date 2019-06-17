import dateutil
import nltk
import preprocessor as p
from wordcloud import WordCloud
from bson.json_util import dumps

nltk.download("punkt")
nltk.download("stopwords")
from nltk.tokenize import TweetTokenizer
import pandas as pd
from collections import Counter
import itertools
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt
import numpy as np
from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
import langdetect as lgt


def retrieve_one_tweet_per_time():

    client = MongoClient(port=27017)
    db = client.european_elections
    collection = db.tweets

    startingDate = '2019-05-20T00:00:00.000Z'
    endingDate = '2019-05-21T00:00:00.000Z'

    myStartingDatetime = dateutil.parser.parse(startingDate)
    myEndingDatetime = dateutil.parser.parse(endingDate)

    cursor = collection.find({
        "date" : {"$gte": myStartingDatetime, "$lt": myEndingDatetime}})

    return cursor


def text_preprocessing(text, language):

    #Introdurre il controllo sulla lingua

    tweets_text = text

    print(len(tweets_text))

    for i in range(0, len(tweets_text)):
        try:
            if lgt.detect(tweets_text.iloc[i]) != "en":

                #print(lgt.detect(tweets_text.iloc[i]))

                tweets_text=tweets_text.drop(tweets_text.index[i])
        except:
            pass

    print(len(tweets_text))

    # Preprocessing TODO:Rimuovere mentions, hashtags e hhtps
    tweets_text = tweets_text.str.lower()
    tweets_text_preprocessed = tweets_text.apply(p.clean)

    # Tokenization
    tokening = TweetTokenizer(strip_handles=True, reduce_len=True)
    tweets_text_preprocessed_tokenized = tweets_text_preprocessed.apply \
        (tokening.tokenize)

    # Rimozione di stopwords e punteggiatura
    stop = stopwords.words(language)
    tweets_tokenized_stop = tweets_text_preprocessed_tokenized.apply \
        (lambda x: [item for item in x if item not in stop])

    punctuation = string.punctuation
    tweets_tokenized_stop_punct = tweets_tokenized_stop.apply \
        (lambda x: [item for item in x if item not in punctuation])

    return tweets_tokenized_stop_punct

#Funzione di conteggio delle parole maggiormente utilizzate
def get_counter(df):
  sentences = (list(itertools.chain(df)))
  flat_list = [item for sublist in sentences for item in sublist]
  c = Counter(flat_list)
  return c

#Funzione di preprocessing con rifinitura
def text_new_processing(tweets, stop):

    tweets_text = tweets
    tweets_text = tweets_text.apply \
        (lambda x: [item for item in x if item not in stop])

    return tweets_text

#Funzione di visulaizzazione a nuvola delle parole più utilizzate
def cloud_visualization(tweets):
    sentences = (list(itertools.chain(tweets)))
    flat_list = [item for sublist in sentences for item in sublist]

    fig = plt.figure(figsize=(20, 14))
    wordcloud = WordCloud(background_color="white").generate(" ".join(flat_list))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Most used words", fontsize=65)
    plt.show()

def histogram_visualization(tweets):
    labels, values = zip(*((get_counter(tweets)).most_common(30)))
    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width, edgecolor='white', color='orange')
    plt.xticks(indexes + width * 0, labels, rotation="vertical")
    plt.title("Most used words", fontsize=20)
    plt.show()

def afinn_visualization(tweets):
    employed_tweets = tweets
    afinn = Afinn()
    pd.options.mode.chained_assignment = None
    employed_tweets["Afinn"] = employed_tweets["text"].apply(afinn.score)
    myDictionary = employed_tweets["Afinn"].value_counts().to_dict()
    plt.bar(myDictionary.keys(), myDictionary.values(), color='orange', edgecolor='white')
    plt.title("Afinn's tweets classification", fontsize=20)
    plt.show()

def vader_visualization(tweets):
    employed_tweets = tweets
    vader = SentimentIntensityAnalyzer()
    employed_tweets["Vader"] = employed_tweets["text"].apply(vader.polarity_scores)
    for i in range(0, len(employed_tweets["Vader"])):
        employed_tweets["Vader"].iloc[i] = (employed_tweets["Vader"].iloc[i]["compound"])
    myDictionary = employed_tweets["Vader"].value_counts().to_dict()
    plt.scatter(myDictionary.keys(), myDictionary.values(), color='orange', edgecolor='white')
    plt.gca().invert_xaxis()
    plt.title("Vader's tweets classification", fontsize=20)
    plt.show()

tweets = retrieve_one_tweet_per_time()
tweets = pd.read_json(dumps(tweets), encoding="ISO-8859-2")
tweets_processed = text_preprocessing(tweets["text"], "english")
print(get_counter(tweets_processed))
new_stopwords = ['’', '...', '…', 'rt', '“', '”', '…', 'u', ':/']
tweets_processed = text_new_processing(tweets_processed, new_stopwords)
print(get_counter(tweets_processed))
cloud_visualization(tweets_processed)
histogram_visualization(tweets_processed)
afinn_visualization(tweets)
vader_visualization(tweets)
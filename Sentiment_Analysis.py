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


def retrieve_one_tweet_per_time():
    client = MongoClient(port=27017)
    db = client.european_elections
    collection = db.tweets

    startingDate = '2019-05-20T00:00:00.000Z'
    endingDate = '2019-05-21T00:00:00.000Z'

    myStartingDatetime = dateutil.parser.parse(startingDate)
    myEndingDatetime = dateutil.parser.parse(endingDate)

    cursor = collection.find({
        "date": {"$gte": myStartingDatetime, "$lt": myEndingDatetime}})

    return cursor


def initial_text_preprocessing(text):
    tweets_text = text

    print(colored("Number of tweets (all languages considered): ", "yellow") + str(len(tweets_text)))

    for i in range(0, len(tweets_text)):

        try:

            if lgt.detect(tweets_text.iloc[i]) != "en":
                tweets_text = tweets_text.drop(tweets_text.index[i])

        except:

            pass

    print(colored("Number of tweets in english: ", "yellow") + str(len(tweets_text)))

    tweets_text = tweets_text.str.lower()
    tweets_text = tweets_text.apply(preproc.clean)

    text_df = pd.DataFrame(columns=["text"])

    text_df["text"] = tweets_text
    return text_df

def refined_text_preprocessing(text, language):

    # Tokenization
    tokening = TweetTokenizer(strip_handles=True, reduce_len=True)
    tweets_text = text.apply(tokening.tokenize)

    # Removing stopwords and punctuation
    stop = stopwords.words(language)
    tweets_text = tweets_text.apply(lambda x: [item for item in x if item not in stop])

    punctuation = string.punctuation
    tweets_text = tweets_text.apply(lambda x: [item for item in x if item not in punctuation])

    return tweets_text

# Most employed words
def words_counter(df):

    sentences = (list(itertools.chain(df)))
    flat_list = [item for sublist in sentences for item in sublist]
    c = Counter(flat_list)
    return c


# Refined preprocessing
def refined_processing(tweets, stop):
    tweets_text = tweets
    tweets_text = tweets_text.apply(lambda x: [item for item in x if item not in stop])

    return tweets_text

# Wordcloud visualization
def cloud_visualization(tweets):
    sentences = (list(itertools.chain(tweets)))
    flat_list = [item for sublist in sentences for item in sublist]

    plt.figure(figsize=(20, 14))
    wordcloud = WordCloud(background_color="white").generate(" ".join(flat_list))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Most used words", fontsize=45)
    plt.show()


def histogram_visualization(tweets):

    labels, values = zip(*((words_counter(tweets)).most_common(30))) # Visualization of the 30 most employed words
    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width, edgecolor='white', color='orange')
    plt.xticks(indexes + width * 0, labels, rotation="vertical")
    plt.title("Most employed words", fontsize=20)
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


def NRC_visualization(tweets):

    '''
    employed_tweets = tweets
    filepath = "./NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
    emolex_df = pd.read_csv(filepath, names=["word", "emotion", "association"], skiprows=45, sep='\t')
    '''

    wordList = defaultdict(list)
    emotionList = defaultdict(list)
    with open('./NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        headerRows = [i for i in range(0, 46)]
        for row in headerRows:
            next(reader)
        for word, emotion, present in reader:
            if int(present) == 1:
                # print(word)
                wordList[word].append(emotion)
                emotionList[emotion].append(word)

    tt = TweetTokenizer()

    def generate_emotion_count(string, tokenizer):
        emoCount = Counter()
        for token in tt.tokenize(string):
            token = token.lower()
            emoCount += Counter(wordList[token])
        return emoCount

    emotionCounts = [generate_emotion_count(tweet, tt) for tweet in tweets]
    emotion_df = pd.DataFrame(emotionCounts, index=tweets.index)
    emotion_df = emotion_df.fillna(0)
    print(emotion_df.head())


    plotting_emotion_dict = {}
    for i in range(0, len(emotion_df.columns)):
        print(emotion_df[emotion_df.columns[i]].sum())
        str(emotion_df.columns[i])
        plotting_emotion_dict[str(emotion_df.columns[i])] = emotion_df[emotion_df.columns[i]].sum()

    print(plotting_emotion_dict)

    lists = sorted(plotting_emotion_dict.items())  # sorted by key, return a list of tuples

    x, y = zip(*lists)  # unpack a list of pairs into two tuples

    plt.bar(x, y, color="orange")
    plt.yscale("log")
    plt.xticks(rotation='vertical')
    plt.title("Emotons distribution")
    plt.xlabel("Emotions")
    plt.ylabel("Number of words")
    plt.show()



original_tweets = retrieve_one_tweet_per_time()
original_tweets = pd.read_json(dumps(original_tweets), encoding="ISO-8859-2")

basic_preprocessed_tweets = initial_text_preprocessing(original_tweets["text"])
'''
tweets = refined_text_preprocessing(basic_preprocessed_tweets["text"], "english")
print(words_counter(tweets))

my_stopwords = ['’', '...', '…', 'rt', '“', '”', '…', 'u', ':/']
tweets = refined_processing(tweets, my_stopwords)
print(words_counter(tweets))

cloud_visualization(tweets)
histogram_visualization(tweets)
afinn_visualization(basic_preprocessed_tweets)
vader_visualization(basic_preprocessed_tweets)
'''

NRC_visualization(basic_preprocessed_tweets["text"])

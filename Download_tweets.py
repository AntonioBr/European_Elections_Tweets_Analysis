import GetOldTweets3 as got
from pymongo import MongoClient
import langdetect as lgt
from datetime import datetime
from datetime import timedelta

def retrive_tweets(search_string, since, until):

    if ((since != "") & (until != "")):

        starting_date = datetime.strptime(since, '%Y-%m-%d')
        ending_time = datetime.strptime(until, '%Y-%m-%d')
        int_time = starting_date + timedelta(days=1)

        while (starting_date != ending_time):

            tweetCriteria = got.manager.TweetCriteria(). \
                setQuerySearch(search_string). \
                setSince(datetime.strftime(starting_date, '%Y-%m-%d')). \
                setUntil(datetime.strftime(int_time, '%Y-%m-%d')).setMaxTweets(300000)

            tweet = got.manager.TweetManager.getTweets(tweetCriteria)

            save_tweets(tweet)
            starting_date = starting_date + timedelta(days=1)
            int_time = starting_date + timedelta(days=1)

    else:

        tweetCriteria = got.manager.TweetCriteria(). \
            setQuerySearch(search_string).setMaxTweets(5)

        tweet = got.manager.TweetManager.getTweets(tweetCriteria)
        save_tweets(tweet)

def save_tweets(tweet):

    client = MongoClient(port=27017)
    db = client.european_elections_tweets
    #db.tweets.drop()

    for f in range(0, len(tweet)):

        date = (tweet[f].date)
        id = (tweet[f].id)
        username = (tweet[f].username)
        text = (tweet[f].text)
        retweets = (tweet[f].retweets)
        favorites = (tweet[f].favorites)
        mentions = (tweet[f].mentions)
        hashtags = (tweet[f].hashtags)
        geo = (tweet[f].geo)
        replies = (tweet[f].replies)
        to = (tweet[f].to)
        try:
            lan = lgt.detect(text)
        except:
            lan = ""

        tweets = {

            'date': date,
            'id': id,
            'username': username,
            'text': text,
            'retweets': retweets,
            'favorites': favorites,
            'mentions': mentions,
            'hashtags': hashtags,
            'geo': geo,
            'replies': replies,
            'to': to,
            'lan': lan

        }

        # Step 3: Insert business object directly into MongoDB via isnert_one
        db.tweets.insert_one(tweets)

    print('Insertion finished.')

def drop_db():
    client = MongoClient(port=27017)
    db = client.european_elections_tweets
    db.tweets.drop()

drop_db()
#retrive_tweets("europe OR #europe OR european elections OR #EuropeanElections OR "
#               "#EuropeanElections2019 OR europe OR #ThisTimeImVoting OR #EUElections2019 OR "
#               "EU elections OR #europeanelections", "2019-05-19", "2019-05-26")

retrive_tweets("european vote", "", "")


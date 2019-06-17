import GetOldTweets3 as got
import networkx as nx
from pymongo import MongoClient
import langdetect as lgt

def retrieve_one_tweet_per_time():

    client = MongoClient(port=27017)
    db = client.european_elections
    collection = db.tweets

    cursor = collection.find({}) #Qui mettere  criteri di ricerca query mongo

    return cursor

def mentions_network_per_language(cursor):

    G = nx.Graph()

    p = 0  # togliere

    for document in cursor:
        if p <= 100: # togliere

            if document["hashtags"] != "":

                hashtags = document["hashtags"].split()

                for j in hashtags:

                    if j not in G:

                        G.add_node(j)

                for i in hashtags:

                    for k in hashtags:

                        if i is not k:

                            if G.has_edge(i, k):

                                G[i][k]["weight"] += (document["favorites"] + document["retweets"])

                            else:

                                G.add_edge(i, k, weight = (document["favorites"] + document["retweets"]))


            p = p + 1

    nx.write_graphml(G, "./hashtags_network.graphml")


mentions_network_per_language(retrieve_one_tweet_per_time())


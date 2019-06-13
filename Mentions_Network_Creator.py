import GetOldTweets3 as got
import networkx as nx
from pymongo import MongoClient
import langdetect as lgt

def retrieve_one_tweet_per_time():

    client = MongoClient(port=27017)
    db = client.european_elections
    collection = db.tweets

    cursor = collection.find({})

    return cursor

def mentions_network(cursor):

    G = nx.DiGraph()

    k = 0 #togliere
    for document in cursor:
        if (k <= 5000): #Da togliere
            mentions_list = []
            if document["mentions"] != "":
                mentions = document["mentions"]
                utilString = ""
                for j in range(0, len(mentions)):
                    if mentions[j] == "@":
                        utilString = ""
                    elif mentions[j] == " ":
                        mentions_list.append(utilString)
                        utilString = ""
                    else:
                        utilString += mentions[j]

                    if (j == len(mentions)-1):
                        mentions_list.append(utilString)

                if document["username"] not in G:

                    G.add_node(document["username"])

                for m in range(0, len(mentions_list)):

                    if mentions_list[m] not in G:

                        G.add_node(mentions_list[m])

                    G.add_edge(document["username"], mentions_list[m])

            k+=1 #togliere

    nx.write_graphml(G, "./mentions_network.graphml")

def mentions_network_per_language(cursor):

    G = nx.DiGraph()

    added = True
    for document in cursor:
        mentions_list = []
        if document["mentions"] != "":
            mentions = document["mentions"]
            utilString = ""
            for j in range(0, len(mentions)):
                if mentions[j] == "@":
                    utilString = ""
                elif mentions[j] == " ":
                    mentions_list.append(utilString)
                    utilString = ""
                else:
                    utilString += mentions[j]

                if (j == len(mentions) - 1):
                    mentions_list.append(utilString)

            if document["username"] not in G:
                if document["lan"] != "":
                    G.add_node(document["username"], language = document["lan"])

                for m in range(0, len(mentions_list)):

                    if mentions_list[m] not in G:

                        try:
                            lan_tweetCriteria = got.manager.TweetCriteria().\
                                setUsername(str(mentions_list[m])).setMaxTweets(1)

                            lan_tweet = got.manager.TweetManager.getTweets(lan_tweetCriteria)
                            G.add_node(mentions_list[m], language = lgt.detect(lan_tweet[0].text))

                        except:
                            added = False
                            pass


                    if added == True:
                        G.add_edge(document["username"], mentions_list[m])

                    added = True

    nx.write_graphml(G, "./mentions_network_language.graphml")


mentions_network(retrieve_one_tweet_per_time())
#mentions_network_per_language(retrieve_one_tweet_per_time())


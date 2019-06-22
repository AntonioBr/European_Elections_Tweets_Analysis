import GetOldTweets3 as got
import dateutil.parser
import networkx as nx
from pymongo import MongoClient
import langdetect as lgt

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

    k = 0  # togliere
    added = True
    for document in cursor:
        print(k)
        #if k <= 1000: #togliere
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

                G.add_node(document["username"], language = document["lan"],
                           text = document["text"])

                for m in range(0, len(mentions_list)):

                    if mentions_list[m] not in G:

                        try:
                            lan_tweetCriteria = got.manager.TweetCriteria().\
                                setUsername(str(mentions_list[m])).setMaxTweets(1)

                            lan_tweet = got.manager.TweetManager.getTweets(lan_tweetCriteria)
                            G.add_node(mentions_list[m], language = lgt.detect(lan_tweet[0].text), text = "")

                        except:
                            added = False
                            pass


                    if added == True:
                        G.add_edge(document["username"], mentions_list[m])

                    added = True

            else:

                #print(G.node[document["username"]]["text"])
                G.node[document["username"]]["text"] = str(G.node[document["username"]]["text"]) + " " + \
                                                       document["text"]

                #print(G.node[document["username"]]["text"])
                for m in range(0, len(mentions_list)):

                    try:
                        lan_tweetCriteria = got.manager.TweetCriteria().\
                            setUsername(str(mentions_list[m])).setMaxTweets(1)

                        lan_tweet = got.manager.TweetManager.getTweets(lan_tweetCriteria)
                        G.add_node(mentions_list[m], language = lgt.detect(lan_tweet[0].text),
                                   text = "")

                    except:
                        added = False
                        pass

                    if added == True:
                        G.add_edge(document["username"], mentions_list[m])

                    added = True

        else:

            if document["username"] not in G:

                G.add_node(document["username"], language = document["lan"],
                           text = document["text"])

            else:

                G.node[document["username"]]["text"] = str(G.node[document["username"]]["text"]) + " " + \
                                                       document["text"]


        k = k + 1 # togliere

    nx.write_graphml(G, "./mentions_network_language.graphml")

#mentions_network(retrieve_one_tweet_per_time())
#obtained_cursor =
mentions_network_per_language(retrieve_one_tweet_per_time())


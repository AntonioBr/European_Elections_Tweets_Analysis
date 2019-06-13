from pymongo import MongoClient


def retrieve_one_tweet_per_time():
    client = MongoClient(port=27017)
    db = client.european_elections
    collection = db.tweets
    cursor = collection.find({}).batch_size(10)
    remove_duplicates(cursor, db, collection)


def remove_duplicates(cursor, db, collection):
    id_list = []

    for document in cursor:

        try:

            if document["id"] not in id_list:

                id_list.append(document["id"])

            else:

                collection.delete_one(document)

        except:

            pass


retrieve_one_tweet_per_time()

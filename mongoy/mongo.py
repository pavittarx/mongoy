from pymongo import MongoClient

class Collection:
    collection = None

    def __init__(self, db, collection):
        self.collection = db[collection]

    def find(self, **args):
        records = []

        if len(args.items()) == 0:
            records = self.collection.find()
        else:
            records = self.collection.find(args['query'])

        docs = []
        for rec in records:
            docs.append(rec)

        return docs

    def insert(self, docs, **kwargs):
        if docs is None:
            raise Exception("Docs Cannot be empty")

        result = None

        if len(kwargs.items()) == 0:
            if type(docs) is list:
                result = self.collection.insert_many(docs)
            else:
                result = self.collection.insert_one(docs)

        if "query" in kwargs:
            if type(docs) is list:
                result = self.collection.insert_many(docs, kwargs["query"])
            else:
                result = self.collection.insert_one(docs, kwargs["query"])

        return result


class Mongo:
    client = None
    db = None

    def __init__(self, connection, database):
        self.client = MongoClient(connection)
        self.db = self.client[database]

    # def use_db(self, database):
    #     self.db = self.client[database]

    def add_collection(self, collection):
        self.__dict__[collection] = Collection(self.db, collection)

    def get_db(self):
        return self.db

    def get_client(self):
        return self.client

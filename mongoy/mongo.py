from datetime import datetime
from pymongo import MongoClient, ReturnDocument

import re
import certifi

class Collection:
    collection = None

    def __init__(self, db, collection):
        self.collection = db[collection]

    def find(self, **args):
        records = []

        if len(args.items()) == 0:
            records = self.collection.find()
        else:
            records = self.collection.find(args["query"])

        docs = []
        for rec in records:
            docs.append(rec)

        return docs

    def insert(self, docs, **kwargs):
        if docs is None:
            raise Exception("Docs Cannot be empty")

        if len(kwargs.items()) == 0:
            if type(docs) is list:
                return self.collection.insert_many(
                    {**docs, "created_at": datetime.now()}
                )
            else:
                return self.collection.insert_one(
                    {**docs, "created_at": datetime.now()}
                )

    def delete(self, query, **kwargs):
        if query is None:
            raise Exception("Query Cannot be empty")

        if "all" in kwargs.items():
            if kwargs["all"] == True:
                return self.collection.delete_many(query)

        return self.collection.delete_one(query)

    def find_one_and_update(self, query, update, **kwargs):
        if query is None:
            raise Exception("Query Cannot be empty")

        if update is None:
            raise Exception("Update Cannot be empty")

        _update = {
            "$set": {
                "updated_at": datetime.now(),
            }
        }

        for key in update.keys():
            if re.search(r"\$.*", key) is not None:
                _update[key] = update[key]
            elif "$set" in _update.keys():
                _update["$set"][key] = update[key]
            else:
                _update["$set"] = {key: update[key]}

        print("Update", _update)

        if len(kwargs.items()) == 0:
            return self.collection.find_one_and_update(
                query, _update, return_document=ReturnDocument.AFTER
            )

        params = {}

        if "upsert" in kwargs.keys():
            if kwargs["upsert"] == True:
                params["upsert"] = True

        return self.collection.find_one_and_update(
            query, _update, return_document=ReturnDocument.AFTER, **params
        )

    def find_all_and_update(self, query, update, **kwargs):
        if query is None:
            raise Exception("Query Cannot be empty")

        if update is None:
            raise Exception("Update Cannot be empty")

        _update = {
            "$set": {
                "updated_at": datetime.now(),
            }
        }

        for key in update.keys():
            if re.search(r"\$.*", key) is not None:
                _update[key] = update[key]
            elif "$set" in _update.keys():
                _update["$set"][key] = update[key]
            else:
                _update["$set"] = {key: update[key]}

        if len(kwargs.items()) == 0:
            return self.collection.update_many(
                query, _update, return_document=ReturnDocument.AFTER
            )

        params = {}

        if "upsert" in kwargs.keys():
            if kwargs["upsert"] == True:
                params["upsert"] = True

        return self.collection.update_many(
            query, _update, return_document=ReturnDocument.AFTER, **params
        )


class Mongo:
    client = None
    db = None

    def __init__(self, connection, database):
        self.client = MongoClient(connection, tlsCAFile=certifi.where())
        self.db = self.client[database]

    # def use_db(self, database):
    #     self.db = self.client[database]

    def register_collection(self, collection):
        self.__dict__[collection] = Collection(self.db, collection)

    def get_db(self):
        return self.db

    def get_client(self):
        return self.client

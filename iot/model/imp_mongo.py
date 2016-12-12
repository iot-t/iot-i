from pymongo import MongoClient

class mongoClient(object):
    KEY_PREFIX = "iot_"
    def __init__(self, url):
        self.mongodb = MongoClient(url)

    def _collection(self, collection):
        return self.mongodb[collection]

    def add_to_collection(self, data, collection):
        ret = self._collection(collection).inser_one(data)
        return ret.inserted_id

    def query_by_filter(self, filters, collection):
        return self._collection(collection).find(filters)

    def update_by_match_field(self, match_field, new_set, collection):
        ret = self._collection(collection).update_many(match_field, new_set)
        return ret.modified_count

    def connectionClose(self):
        # close on every incoming request ?
        # FIXME
        self.mongodb.close()


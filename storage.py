import json
from abc import ABC, abstractmethod

from mongo import MongoDatabase


class StorageAbstract(ABC):

    @abstractmethod
    def store(self, data, *args):
        pass

    @abstractmethod
    def loader(self, *args, **kwargs):
        pass


class MongoStorage(StorageAbstract):

    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self, data, source=None, collection=None):
        collection = getattr(self.mongo.database, collection)
        if isinstance(data, list) and len(data) > 1 :
            collection.insert_many(data)
        else:
            collection.insert_one(data)

    def loader(self, collection_name, filter_data=None):
        collection = self.mongo.database[collection_name]
        if filter_data is not None:
            data = collection.find(filter_data)
        else:
            data = collection.find()
        return data

    def update_flag(self, data):
        """
        To prevent from crawling again those we already have:
        if a link's flag is true , it means
        we do not apply extract_pages method on it
        """
        self.mongo.database.advertisements_links.find_one_and_update({'_id': data['_id']},{'$set': {'flag': True}})


class FileStorage(StorageAbstract):

    def store(self, data, source=None, *args):
        if source == "results/":
            filename = "data"
        else:
            filename = data.get('post_id', 'sample')

        with open(f'{source}{filename}.json', 'w') as f:
            f.write(json.dumps(data))

    def loader(self, *args, **kwargs):
        with open('results/data.json', 'r') as f:
            links = json.loads(f.read())
        return links

    def update_flag(self, data):
        pass

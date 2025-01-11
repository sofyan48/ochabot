from pymongo import MongoClient
from urllib.parse import quote_plus
import os

class MongoDB:
    def __init__(self, host='localhost', port=27017, username='admin', password="", database="mydb"):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.mongo_url = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}:{port}"
        try:
            self.client = MongoClient(self.mongo_url)
            self.db = self.client[database]
        except Exception as e:
            raise e

    def get_url(self):
        return self.mongo_url
    def knowledge_history_collection(self):
        return self.db[os.environ.get("KNOWLEDGE_BASE_MONGO_COLLECTION")]
    
    def set_collection(self, collection):
        return self.db[collection]
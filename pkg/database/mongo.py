from motor.motor_asyncio import AsyncIOMotorClient 
  
class MongoDB:  
    _instance = None  
    _client = None  
    _database = None  
  
    def __new__(cls, uri: str, database_name: str):  
        if cls._instance is None:  
            cls._instance = super(MongoDB, cls).__new__(cls)  
            cls._instance._client = AsyncIOMotorClient(uri)  
            cls._instance._database = cls._instance._client[database_name]  
        return cls._instance  
  
    def get_collection(self, collection_name: str):  
        return self._database[collection_name]  
  
    @classmethod  
    def get_instance(cls, uri: str, database_name: str):  
        if cls._instance is None:  
            cls._instance = cls(uri, database_name)  
        return cls._instance  
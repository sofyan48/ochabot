from elasticsearch import Elasticsearch
from threading import Lock
from pkg.database import ElasticConfig

class ElasticConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ElasticConnection, cls).__new__(cls)
        return cls._instance

    
    def connection_url(config: ElasticConfig):
        cfg = config.get_config()
        connection_str = "http://{}:{}".format(
            cfg.get("host"),
            cfg.get("port"),
        )
        return connection_str

    @classmethod
    def initialize(cls, config: ElasticConfig):
        if not hasattr(cls._instance, 'client'):
            cfg = config.get_config()
            conn_url = cls.connection_url(config=config)
            cls._instance = Elasticsearch(
                hosts=conn_url,
                http_auth=(cfg.get("user"), cfg.get("password"))
            )

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            raise Exception("ElasticConnection is not initialized. Call initialize() first.")
        return cls._instance

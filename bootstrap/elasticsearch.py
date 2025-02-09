from pkg.database.elasticsearch import ElasticConnection
from pkg.database import ElasticConfig
import os

def register_elasticsearch():
    cfg = ElasticConfig(
        user=os.getenv("ELASTIC_USER"),
        password=os.getenv("ELASTIC_PASSWORD"),
        host=os.getenv("ELASTIC_HOST"),
        port=os.getenv("ELASTIC_PORT"),
    )
    
    ElasticConnection.initialize(cfg)
    return ElasticConnection.get_client()
from pkg.vectorstore.chromadb import ChromaDB
from pkg.vectorstore.elasticsearch import ElasticsearcVector
from pkg.logger.logging import logger

class Vectorstores(object):
    def __init__(self):
        pass

    def configure(self, vectorestore = None) -> ChromaDB | ElasticsearcVector:
        
        if vectorestore is None:
            if ChromaDB._chroma is None:
                logger.error("ChromaDB not connect, please import or declare on init")
                raise "Chroma not connect"
            return ChromaDB
        
        if vectorestore=="elastic":
            if ElasticsearcVector._elastic is None:
                logger.error("Elasticsearch not connect, please import or declare on init")
                raise "Elasticsearch not connect"
            return ElasticsearcVector
        else:
            return ChromaDB

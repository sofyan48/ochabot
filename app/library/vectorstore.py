from pkg.vectorstore.chromadb import ChromaDB
from pkg.vectorstore.elasticsearch import ElasticsearcVector
from pkg.logger.logging import logger

class Vectorstores(object):
    def __init__(self):
        pass

    def chroma_client(self):
        if ChromaDB._chroma is None:
                logger.error("ChromaDB not connect, please import or declare on init")
                raise "Chroma not connect"
        return ChromaDB
    
    def elastic_client(self):
        if ElasticsearcVector._elastic is None:
            logger.error("Elasticsearch not connect, please import or declare on init")
            raise "Elasticsearch not connect"
        return ElasticsearcVector

    def configure(self, vectorestore = None) -> ChromaDB | ElasticsearcVector:
        if vectorestore is None:
            return self.chroma_client()
        
        if vectorestore=="elasticsearch":
            return self.elastic_client()
        else:
            return self.chroma_client()
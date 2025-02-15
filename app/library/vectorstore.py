from pkg.vectorstore.chromadb import ChromaDB
from pkg.vectorstore.elasticsearch import ElasticsearcVector
from pkg.logger.logging import logger

class Vectorstores(object):
    def __init__(self):
        self.client = None

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
            self.client = self.chroma_client()
        
        if vectorestore=="elasticsearch":
            self.client = self.elastic_client()
        else:
            self.client = self.chroma_client()
        return self.client
        
    def retriever(self, vectorDB, top_k, fetch_k, collection):
        self.client.retriever(vector=vectorDB,
            top_k=top_k,
            fetch_k=fetch_k,
            collection=collection,)
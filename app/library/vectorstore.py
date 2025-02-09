from pkg.vectorstore.chromadb import ChromaDB
from pkg.vectorstore.elasticsearch import ElasticsearcVector


class Vectorstores(object):
    def __init__(self):
        pass

    def configure(self, vectorestore = None) -> ChromaDB | ElasticsearcVector:
        if vectorestore is None:
            return ChromaDB
        
        if vectorestore=="elastic":
            return ElasticsearcVector
        else:
            return ChromaDB

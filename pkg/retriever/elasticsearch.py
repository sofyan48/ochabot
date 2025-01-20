from langchain_elasticsearch import ElasticsearchStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import VectorStoreRetriever
from pkg.embedding.mistral import MistralInference
import os

class ElasticsearcVector(object):
    def __init__(self, topK, fetchK , host, port, user,password, index, embbedding=None):
        es_uri = host+":"+port
        self.index = index
        self.embeddings = embbedding
        if embbedding is None:
            self.apikey = os.getenv("MISTRAL_API_KEY")
            self.embeddings = MistralInference(apikey=self.apikey)
        try:
            self.elastic = ElasticsearchStore(
                es_url=es_uri,
                index_name=index,
                embedding=embbedding,
                es_user=user,
                es_password=password,
            )
        except Exception as e:
            raise e
        self.topK = topK
        self.fetchK = fetchK
    
    def build(self, data, chunk=2000, overlap=500):
        if self.embbedding is None:
            return "please add embedding"
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk, chunk_overlap=overlap)
        all_splits = text_splitter.split_documents(data)
        return self.elastic.from_documents(
            documents=all_splits, 
            embedding=self.embeddings,
        )

    def retriever(self, topK, fecthK: int = 0) -> VectorStoreRetriever:
        if (topK != 0):
            self.topK = topK
        if (fecthK != 0):
            self.fetchK = topK

        return self.elastic.as_retriever(
            search_type="mmr",
            search_kwargs={
                'k': self.topK, 
                'fetch_k': self.fetchK
            }
        )
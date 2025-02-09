from langchain_elasticsearch import ElasticsearchStore  
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain_core.vectorstores import VectorStoreRetriever  
from pkg.embedding.mistral import MistralInference  
import os  
  
class ElasticsearcVector:  
    _instance = None  
    _topK = 0  
    _fetchK = 0  
    _host = ""  
    _port = ""  
    _user = ""  
    _password = ""  
    _index = ""  
    _embeddings = None  
    _elastic = None  
  
    @classmethod  
    def configure(cls, topK: int, fetchK: int, host: str, port: str, user: str, password: str, index: str, embedding=None):  
        """Method to configure the Elasticsearch vector store settings."""  
        cls._topK = topK  
        cls._fetchK = fetchK  
        cls._host = host  
        cls._port = port  
        cls._user = user  
        cls._password = password  
        cls._index = index  
          
        es_uri = f"{cls._host}:{cls._port}"  
        if embedding is None:  
            cls._apikey = os.getenv("MISTRAL_API_KEY")  
            cls._embeddings = MistralInference(apikey=cls._apikey)  
        else:  
            cls._embeddings = embedding  
          
        try:  
            cls._elastic = ElasticsearchStore(  
                es_url=es_uri,  
                index_name=cls._index,  
                embedding=cls._embeddings,  
                es_user=cls._user,  
                es_password=cls._password,  
            )  
        except Exception as e:
            raise e  
  
    @classmethod  
    def build(cls, data, collection, chunk=2000, overlap=500):  
        if cls._embeddings is None:  
            return "please add embedding"  
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk, chunk_overlap=overlap)  
        all_splits = text_splitter.split_documents(data)
        es_uri = f"{cls._host}:{cls._port}"
        return cls._elastic.from_documents(  
            documents=all_splits,   
            embedding=cls._embeddings,
            index_name=collection,
            es_url=es_uri, 
            es_user=cls._user,  
            es_password=cls._password,
        )  
  
    @classmethod  
    def retriever(cls, topK: int = 0, fetchK: int = 0) -> VectorStoreRetriever:  
        if topK != 0:  
            cls._topK = topK  
        if fetchK != 0:  
            cls._fetchK = fetchK  
  
        return cls._elastic.as_retriever(  
            search_type="mmr",  
            search_kwargs={  
                'k': cls._topK,   
                'fetch_k': cls._fetchK  
            }  
        )  

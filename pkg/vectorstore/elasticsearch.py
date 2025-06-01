from langchain_elasticsearch import ElasticsearchStore  
from pkg.vectorstore.splitter import TextSplitter
from pkg.vectorstore import VectorStoreRetriever  
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
    _es_uri = None
    _text_splitter = TextSplitter()
  
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
        cls._es_uri = es_uri
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
        docs_split = cls._text_splitter.text_splitter(data=data, chunk=chunk, overlap=overlap)
        es_uri = f"{cls._host}:{cls._port}"
        return cls._elastic.from_documents(  
            documents=docs_split,   
            embedding=cls._embeddings,
            index_name=collection,
            es_url=es_uri, 
            es_user=cls._user,  
            es_password=cls._password,
        )  
  
    @classmethod  
    def retriever(cls, topK: int = 0, fetchK: int = 0, collection: str = "") -> VectorStoreRetriever:  
        if topK != 0:  
            cls._topK = topK  
        if fetchK != 0:  
            cls._fetchK = fetchK
        
        try: 
            # model seperti ini karena fungsi as_retriever() tidak bisa menerima parameter collection choice 
            elastic = ElasticsearchStore(  
                es_url=cls._es_uri,  
                index_name=collection,  
                embedding=cls._embeddings,  
                es_user=cls._user,  
                es_password=cls._password,  
            )  
            return elastic.as_retriever(
                search_type="mmr",  
                search_kwargs={  
                    'k': cls._topK,   
                    'fetch_k': cls._fetchK  
                },
                index_name=collection,
                collection=collection,
            )
        except Exception as e:
            raise e
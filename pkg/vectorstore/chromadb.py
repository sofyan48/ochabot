from pkg.vectorstore.splitter import TextSplitter
from langchain_chroma import Chroma  
from chromadb import HttpClient 
from chromadb.config import DEFAULT_DATABASE, DEFAULT_TENANT
from chromadb.config import Settings  
from pkg.embedding.mistral import MistralInference  
from pkg.vectorstore import VectorStoreRetriever
from pkg.logger.logging import logger
import os  
  
class ChromaDB:  
    _instance = None  
    _topK = 0  
    _fetchK = 0  
    _host = ""  
    _port = 0  
    _embeddings = None  
    _chroma = None  
    _text_splitter = TextSplitter()
  
    def __new__(cls, *args, **kwargs):  
        if cls._instance is None:  
            cls._instance = super(ChromaDB, cls).__new__(cls)  
        return cls._instance  
  
    @classmethod  
    def configure(cls, topK: int, fetchK: int, host: str, port: int, embedding=None, tenant=None, database=None):  
        """Method to configure the retriever settings."""  
        cls._topK = topK  
        cls._fetchK = fetchK  
        cls._host = host  
        cls._port = port  
          
        if embedding is None:  
            cls._apikey = os.getenv("MISTRAL_API_KEY")  
            cls._embeddings = MistralInference(apikey=cls._apikey)  
        else:  
            cls._embeddings = embedding  

        if tenant is None:
            tenant = DEFAULT_TENANT

        if database is None:
            database = DEFAULT_DATABASE

        try:  
            chroma_settings = Settings(  
                chroma_api_impl="chromadb.api.segment.SegmentAPI",  
                chroma_server_cors_allow_origins=[],  
                allow_reset=True  
            )  
            cls._chroma = HttpClient(  
                host=cls._host,  
                port=cls._port,  
                settings=chroma_settings,
                tenant=tenant,
                database=database
            )  
        except Exception as e:  
            raise e  
    
    @classmethod  
    def build(cls, data, collection, chunk=2000, overlap=500):
        docs_split = cls._text_splitter.text_splitter(data=data, chunk=chunk, overlap=overlap)
        return Chroma.from_documents(  
            documents=docs_split,   
            embedding=cls._embeddings,   
            client=cls._chroma,  
            collection_name=collection  
        )  
  
    @classmethod  
    def retriever(cls, topK: int = 0, fetchK: int = 0, collection: str = "") -> VectorStoreRetriever:  
        if topK != 0:  
            cls._topK = topK  
        if fetchK != 0:  
            cls._fetchK = fetchK  
              
        try:  
            crm = Chroma(  
                client=cls._chroma,  
                embedding_function=cls._embeddings,  
                collection_name=collection  
            )  
        except Exception as e:  
            raise e  
              
        return crm.as_retriever(  
            search_type="mmr",  
            search_kwargs={  
                'k': cls._topK,   
                'fetch_k': cls._fetchK  
            }  
        )  

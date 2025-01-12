from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from chromadb import HttpClient
from chromadb.config import Settings
from pkg.logger.logging import logger
from pkg.embedding.huggingface import HuggingfaceInference
import os


# Unique identifier for the Chroma client
identifier = "unique_identifier"

class Retriever():
    def __init__(self, host="", port=8000, apikey="") -> None:
        self.embeddings = HuggingfaceInference(apikey=apikey).embeddings()
        try: 
            chroma_settings = Settings(
                chroma_api_impl = "chromadb.api.segment.SegmentAPI",
                chroma_server_cors_allow_origins=[],
                allow_reset=True
            )
            self.chroma = HttpClient(
                host=host,
                port=port,
                settings=chroma_settings
            )
        except Exception as e:
            
            raise e
        
        
    def build(self, data, collection, chunk=400):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk)
        all_splits = text_splitter.split_documents(data)
        return Chroma.from_documents(
            documents=all_splits, 
            embedding=self.embeddings, 
            client=self.chroma,
            collection_name=collection
        )

    def retriever(self, topK, fecthK: int, collection: str):
        crm = Chroma(
            client=self.chroma,
            embedding_function=self.embeddings,
            collection_name=collection
        )
        return crm.as_retriever(
            search_type="mmr",
            search_kwargs={
                'k': topK, 
                'fetch_k': fecthK
            }
        )
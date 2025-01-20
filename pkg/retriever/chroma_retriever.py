from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from chromadb import HttpClient
from chromadb.config import Settings
from pkg.embedding.mistral import MistralInference
from langchain_core.vectorstores import VectorStoreRetriever
import os

class Retriever():
    def __init__(self, topK, fetchK , host, port, embbedding=None) -> None:
        self.embeddings = embbedding
        if embbedding is None:
            self.apikey = os.getenv("MISTRAL_API_KEY")
            self.embeddings = MistralInference(apikey=self.apikey)
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
        self.topK = topK
        self.fetchK = fetchK
        
    def build(self, data, collection, chunk=2000, overlap=500):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk, chunk_overlap=overlap)
        all_splits = text_splitter.split_documents(data)
        return Chroma.from_documents(
            documents=all_splits, 
            embedding=self.embeddings, 
            client=self.chroma,
            collection_name=collection
        )

    def retriever(self, topK, fecthK: int = 0, collection: str = "") -> VectorStoreRetriever:
        if (topK != 0):
            self.topK = topK
        if (fecthK != 0):
            self.fetchK = topK
        try:
            crm = Chroma(
                client=self.chroma,
                embedding_function=self.embeddings,
                collection_name=collection
            )
        except Exception as e:
            raise e
        return crm.as_retriever(
            search_type="mmr",
            search_kwargs={
                'k': self.topK, 
                'fetch_k': self.fetchK
            }
        )
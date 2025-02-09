
from pkg.vectorstore.chromadb import ChromaDB
from pkg.vectorstore.elasticsearch import ElasticsearcVector
from pkg.embedding.mistral import MistralInference
import os

def register_chroma_retriever():
    try:
        return ChromaDB().configure(
            topK=int(os.getenv("RETRIEVER_TOPK")),
            fetchK=int(os.getenv("RETRIEVER_FETCHK")),
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=int(os.getenv("CHROMA_PORT", 8000)),
            embedding=MistralInference(
                apikey=os.getenv("MISTRAL_API_KEY")
            ).embeddings()
        )
    except Exception as e:
        raise e
    
def register_elasticsearch_vectorstore():
    ElasticsearcVector.configure(
        topK=int(os.getenv("RETRIEVER_TOPK")),
        fetchK=int(os.getenv("RETRIEVER_FETCHK")),
        user=os.getenv("ELASTIC_USER"),
        password=os.getenv("ELASTIC_PASSWORD"),
        host=os.getenv("ELASTIC_HOST"),
        port=os.getenv("ELASTIC_PORT"),
        index=os.getenv("ELASTIC_COLLECTION"),
        embedding=MistralInference(
            apikey=os.getenv("MISTRAL_API_KEY")
        ).embeddings()
    )
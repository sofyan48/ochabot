
from pkg.vectorstore.chromadb import ChromaDB
from pkg.vectorstore.elasticsearch import ElasticsearcVector
from pkg.embedding.mistral import MistralInference
from pkg.logger.logging import logger
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
    host = "{}".format(
        os.getenv("ELASTIC_HOST", "localhost")
    )
    try:
        return ElasticsearcVector.configure(
            topK=int(os.getenv("RETRIEVER_TOPK")),
            fetchK=int(os.getenv("RETRIEVER_FETCHK")),
            user=os.getenv("ELASTIC_USER"),
            password=os.getenv("ELASTIC_PASSWORD"),
            host=host,
            port=os.getenv("ELASTIC_PORT", "9200"),
            index=os.getenv("ELASTIC_COLLECTION", "ochabot"),
            embedding=MistralInference(
                apikey=os.getenv("MISTRAL_API_KEY")
            ).embeddings()
        )
    except Exception as e:
        logger.warning("Cannot to elastic server",{
            "error": e
        })
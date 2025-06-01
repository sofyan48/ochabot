
from pkg.vectorstore.chromadb import ChromaDB
from pkg.vectorstore.elasticsearch import ElasticsearcVector
from pkg.embedding.mistral import MistralInference
from pkg.embedding.nvidia import NvidiaEmbedding
from pkg.embedding.openai import OpenAIEmbedding
from pkg.embedding.huggingface import HuggingfaceInference
from pkg.logger.logging import logger
import os

def embeddings(embedding=None):
    if embedding == "mistral":
        return MistralInference(
            apikey=os.getenv("MISTRAL_API_KEY")
        ).embeddings()
    elif embedding == "huggingface":
        return HuggingfaceInference(
            apikey=os.getenv("HUGGINGFACE_API_KEY"),
            model=os.getenv("HUGGINGFACE_MODEL", "sentence-transformers/all-mpnet-base-v2")
        ).embeddings()
    elif embedding == "nvidia":
        return NvidiaEmbedding(
            model=os.getenv("NVIDIA_EMBEDDING_MODEL", "NV-Embed-QA"),
            apikey=os.getenv("NVIDIA_API_KEY")
        ).embeddings()
    elif embedding == "openai":
        return OpenAIEmbedding(
            model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            apikey=os.getenv("OPENAI_API_KEY")
        ).embeddings()
    
    return  MistralInference(
            apikey=os.getenv("MISTRAL_API_KEY")
        ).embeddings()

def register_chroma_retriever():
    try:
        return ChromaDB().configure(
            topK=int(os.getenv("RETRIEVER_TOPK")),
            fetchK=int(os.getenv("RETRIEVER_FETCHK")),
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=int(os.getenv("CHROMA_PORT", 8000)),
            embedding=embeddings(
                os.getenv("EMBEDDING_TYPE", "mistral")
            ),
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
            index=os.getenv("ELASTIC_COLLECTION", "gnm-gpt-analyzer-srvc"),
            embedding=embeddings(
                os.getenv("EMBEDDING_TYPE", "mistral")
            ),
        )
    except Exception as e:
        logger.warning("Cannot to elastic server",{
            "error": e
        })
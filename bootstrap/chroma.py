
from pkg.chromadb import ChromaDB
from pkg.embedding.mistral import MistralInference
from pkg.embedding.huggingface import HuggingfaceInference
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
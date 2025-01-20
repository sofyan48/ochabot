
from pkg.retriever.chroma_retriever import Retriever
from pkg.embedding.mistral import MistralInference
from pkg.embedding.huggingface import HuggingfaceInference
import os

def register_chroma_retriever():
    try:
        return Retriever(
                topK=int(os.getenv("RETRIEVER_TOPK")),
                fetchK=int(os.getenv("RETRIEVER_FETCHK")),
                host=os.getenv("CHROMA_HOST", "localhost"),
                port=int(os.getenv("CHROMA_PORT", 8000)),
                # embbedding=MistralInference(
                #     apikey=os.getenv("MISTRAL_API_KEY")
                # ).embeddings() 
                embbedding=HuggingfaceInference(
                    apikey=os.getenv("HUGGING_FACE_APIKEY")
                ).embeddings()
            )
    except Exception as e:
        raise e
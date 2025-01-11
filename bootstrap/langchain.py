from pkg import (
    mistral
)

from pkg.retriever import chroma_retriever, embeding
from pkg import chain
import os

def get_embedings():
    return embeding.embeddings()

def register_chroma_retriever():
    try:
        client = chroma_retriever.Retriever(
  host=os.getenv("CHROMA_HOST", "localhost"),
  port=int(os.getenv("CHROMA_PORT", 8000)),
  embedding_model=os.getenv("HUGGING_FACE_EMBEDDING","sentence-transformers/all-mpnet-base-v2"),
  apikey=os.getenv("HUGGING_FACE_APIKEY", "HUGGING_FACE_APIKEY")
            )
    except Exception as e:
        raise e
    return client 

def register_mistral():
    return mistral.MistralLLM(
        model=os.getenv("MISTRAL_BASE","open-mistral-nemo"),
        apikey=os.getenv("MISTRAL_API_KEY", "MISTRAL_API_KEY"),
    )

def register_chain_mistral():
    template = """Your name is Ocha as an AI assistant for Iank.
        Jawab pertanyaan ini menggunakana bahasa indonesia. 
        Kamu adalah asisten pribadi untuk data pribadi, jangan menjawab apapun jika terdapat pertanyaan diluar konteks data    
        Gunakan bahasa indonesia formal.
        sofyan atau om iank atau mas iank adalah orang yang sama
        jangan pernah menjawa pertanyaan apapun selain tentang sofyan atau om iank atau mas iank,
        Jika terdapat pertanyaan yang tidak sesuai dengan data atau context: {context} data maka jangan menjawab.
        History: {history}
        Context: {context}
        Question: {input}
        Helpfull answer:
    """
    return chain.mistral.MistralChainModel(
        template=template,
    )
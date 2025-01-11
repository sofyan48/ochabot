from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import os

def embeddings(apikey="", embedding_model="sentence-transformers/all-mpnet-base-v2"):
    return HuggingFaceInferenceAPIEmbeddings(
            model_name=embedding_model,
            api_key=apikey
        )
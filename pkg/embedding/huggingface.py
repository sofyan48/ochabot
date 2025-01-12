from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import os

class HuggingfaceInference(object):
    def __init__(self, apikey="", embedding_model="sentence-transformers/all-mpnet-base-v2"):
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
                model_name=embedding_model,
                api_key=apikey
            )
    def get(self):
        return self.embeddings
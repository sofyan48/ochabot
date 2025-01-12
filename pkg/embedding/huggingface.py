from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

class HuggingfaceInference(object):
    def __init__(self, apikey="", embedding_model="sentence-transformers/all-mpnet-base-v2"):
        self.apikey = apikey
        self.embedding_model = embedding_model
    
    def embeddings(self) -> HuggingFaceInferenceAPIEmbeddings:
        return HuggingFaceInferenceAPIEmbeddings(
                model_name=self.embedding_model,
                api_key=self.apikey
            )
from langchain_mistralai import MistralAIEmbeddings

class MistralInference(object):
    def __init__(self, model=None, apikey="") -> None:
        if model == "":
            model = "mistral-embed"
        self.model = model
        self.apikey = apikey

    def embeddings(self):
        return MistralAIEmbeddings(api_key=self.apikey)
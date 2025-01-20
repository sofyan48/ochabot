from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings


class NvidiaEmbedding(object):
    def __init__(self, model=None, apikey="") -> None:
        if model == "" or model is None:
            model = "NV-Embed-QA"
        self.model = model
        self.apikey = apikey

    def embeddings(self):
        return NVIDIAEmbeddings(
            model=self.model,
            api_key=self.apikey
        )
    
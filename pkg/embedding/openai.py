from langchain_community.embeddings import OpenAIEmbeddings

class OpenAIEmbedding:
    _instance = None
    _embeddings = None

    @classmethod
    def configure(cls, api_key: str, model_name: str = "text-embedding-3-small"):
        """Method to configure the OpenAI embeddings settings."""
        cls._embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model=model_name
        )

    @classmethod
    def get_embeddings(cls):
        """Method to get the configured OpenAI embeddings instance."""
        if cls._embeddings is None:
            raise ValueError("OpenAI embeddings have not been configured. Please call configure() first.")
        return cls._embeddings
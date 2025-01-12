
from langchain_community.cache import SQLAlchemyCache
from langchain.globals import set_llm_cache
from langchain_mistralai.chat_models import ChatMistralAI 
from langchain_redis import RedisCache, RedisSemanticCache


class MistralLLM():
    def __init__(self, model:str, apikey:str) -> None:
        if model == "":
            model = "mistral-large-latest"
        self.model = model
        self.apikey = apikey

    def run(self, redis_url, embedings) -> ChatMistralAI:
        # redis_cache = RedisSemanticCache(redis_url=redis_url, ttl=14400, embeddings=embedings, distance_threshold=0.2)
        redis_cache = RedisCache(redis_url=redis_url, ttl=14400)
        set_llm_cache(redis_cache)
        return ChatMistralAI(
            cache=True,
            model_name=self.model,
            mistral_api_key=self.apikey,
            temperature=0.6,
            top_k=8,
            top_p=0.7,
            tfs_z=2.0,
        )
         
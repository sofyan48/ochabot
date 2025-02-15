from pkg.ollama import OllamaPlatform, OllamaLLM
from app import redis

class OllamaLibrary(object):
    def __init__(self, llm: OllamaPlatform, model: str, redis: redis, base_url=None, top_k=4, top_p=0.2):
        self.ollama = llm
        self.model = model
        self.redis = redis
        self.top_p = top_p
        self.top_k = top_k
        self.base_url = base_url
    
   
    def get_llm(self, model) -> OllamaLLM:
        try:
            return self.ollama.run(
                base_url=self.base_url,
                top_k = self.top_k,
                top_p=self.top_p,
                redis_url=self.redis.str_conn(),
                model=model
            )
        except Exception as e:
            raise e
from pkg.mistral import MistralLLM, ChatMistralAI
from app import redis

class MistralAILibrary(object):
    def __init__(self, llm: MistralLLM, model: str, redis: redis):
        self.mistral = llm
        self.redis = redis
        self.model = model
    
    def run(self, model) -> ChatMistralAI:
        try:
            return self.mistral.run(
                redis_url=self.redis.str_conn(),
                model=model
            )
        except Exception as e:
            raise e
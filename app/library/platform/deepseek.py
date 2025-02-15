from pkg.deepseek import DeepSeekLLM, ChatOpenAI
from app import redis


class DeepSeekLibrary(object):
    def __init__(self, llm: DeepSeekLLM, model: str, redis: redis):
        self.deepseek = llm
        self.model = model
        self.redis = redis
    
    def run(self, model) -> ChatOpenAI:
        try:
            return self.deepseek.run(
                redis_url=self.redis.str_conn(),
                model=model
            )
        except Exception as e:
            raise e
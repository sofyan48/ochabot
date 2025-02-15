from pkg.openai import OpenAILLM, ChatOpenAI
from app import redis

class OpenAILibrary(object):
    def __init__(self, llm: OpenAILLM, model: str, redis: redis):
        self.openai = llm
        self.model = model
        self.redis = redis
    
    def run(self, model) -> ChatOpenAI:
        try:
            return self.openai.run(
                redis_url=self.redis.str_conn(),
                model=model
            )
        except Exception as e:
            raise e
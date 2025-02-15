from pkg.groq import GroqLLM, ChatGroq
from app import redis

class GroqAILibrary(object):
    def __init__(self, llm: GroqLLM, model: str, redis: redis):
        self.groq = llm
        self.model = model
        self.redis = redis

    def run(self, model) -> ChatGroq:
        try:
            return self.groq.run(
                redis_url=self.redis.str_conn(),
                model=model
            )
        except Exception as e:
            raise e
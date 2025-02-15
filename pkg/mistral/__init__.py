from langchain.globals import set_llm_cache  
from langchain_mistralai.chat_models import ChatMistralAI   
from langchain_redis import RedisCache 


class MistralLLM:  
    _instance = None  
    _model = "mistral-large-latest"  
    _apikey = ""
  
    def __new__(cls, *args, **kwargs):  
        if cls._instance is None:  
            cls._instance = super(MistralLLM, cls).__new__(cls)  
        return cls._instance  
  
    @classmethod  
    def configure(cls, model: str = "open-mistral-nemo", apikey: str = "", template: str = ""):  
        if cls._instance is None:  
            cls._instance = super(MistralLLM, cls).__new__(cls)  
        cls._model = model if model else cls._model  
        cls._apikey = apikey if apikey else cls._apikey  
        cls._template = template if template else cls._template  
        return cls._instance  
  
    @classmethod  
    def run(cls, redis_url: str = "", model: str = None) -> ChatMistralAI:  
        cache = False  
        if redis_url != "":  
            redis_cache = RedisCache(redis_url=redis_url, ttl=14400)  
            set_llm_cache(redis_cache)  
            cache = True  
  
        if model is not None:  
            cls._model = model  
  
        return ChatMistralAI(  
            cache=cache,  
            model_name=cls._model,  
            mistral_api_key=cls._apikey,  
            temperature=0.6,  
            top_k=5,  
            top_p=0.8,  
            tfs_z=2.0,  
        )  

from langchain_openai.chat_models import ChatOpenAI  
from langchain.globals import set_llm_cache  
from langchain_redis import RedisCache 


class OpenAILLM(object):  
    _instance = None    
    _model = "gpt-4o-mini"    
    _apikey = ""
    _llm: ChatOpenAI = None

    def __new__(cls, *args, **kwargs):    
        if cls._instance is None:    
            cls._instance = super(OpenAILLM, cls).__new__(cls)    
        return cls._instance    
      
    @classmethod  
    def configure(cls, model: str = "gpt-4o-mini", apikey: str = "", template: str = ""):  
        """Method to configure the model, API key, and template."""  
        cls._model = model if model else cls._model  
        cls._apikey = apikey if apikey else cls._apikey  
        cls._template = template if template else cls._template  
  
    @classmethod  
    def run(cls, redis_url: str = "", model: str = None) -> ChatOpenAI:  
        cache = False  
        if redis_url != "":  
            redis_cache = RedisCache(redis_url=redis_url, ttl=14400)  
            set_llm_cache(redis_cache)  
            cache = False  
  
        if model is not None:  
            cls._model = model  

        cls._llm = ChatOpenAI(  
            cache=cache,  
            model=cls._model,  
            temperature=0.4,  
            max_tokens=None,  
            timeout=None,  
            max_retries=2,  
            top_p=0.8,  
            api_key=cls._apikey,  
            presence_penalty=0.8,  
            frequency_penalty=0.8  
        )
        return cls._llm
from langchain_openai.chat_models import ChatOpenAI  
from langchain.globals import set_llm_cache  
from langchain_redis import RedisCache 
from openai import OpenAI


class OpenAIDirect(object):
    _instance = None
    _model = "gpt-4o-mini"    
    _apikey = ""
    
    def __new__(cls, *args, **kwargs):    
        if cls._instance is None:    
            cls._instance = super(OpenAIDirect, cls).__new__(cls)
        return cls._instance    
    
    @classmethod  
    def configure(cls, apikey: str = ""):  
        cls._instance = OpenAI(api_key=apikey)
        return cls._instance
    
    @classmethod
    def text_to_speech(cls, input: str, model="tts-1"):
        return cls._instance.audio.speech.create(
            model=model,
            voice="alloy",
            input=input
        )



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
        if redis_url != "":
            redis_cache = RedisCache(redis_url=redis_url, ttl=14400)  
            set_llm_cache(redis_cache)  
  
        if model is not None:  
            cls._model = model  

        cls._llm = ChatOpenAI(  
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
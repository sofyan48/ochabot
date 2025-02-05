from langchain_openai.chat_models import ChatOpenAI  
from langchain.globals import set_llm_cache  
from langchain_redis import RedisCache  
from langchain.chains.combine_documents import create_stuff_documents_chain  
from langchain_core.vectorstores import VectorStoreRetriever  
from langchain_core.prompts import PromptTemplate  
from langchain.chains.retrieval import Runnable, create_retrieval_chain  
from pkg.chain.prompter import DefaultPrompter  

class DeepSeekLLM(object):  
    _instance = None    
    _model = "deepseek-chat	"    
    _apikey = ""    
    _template = DefaultPrompter.default_prompter()
    
    def __new__(cls, *args, **kwargs):    
        if cls._instance is None:    
            cls._instance = super(DeepSeekLLM, cls).__new__(cls)    
        return cls._instance    
      
    @classmethod  
    def configure(cls, model: str = "deepseek-chat", apikey: str = "", template: str = ""):  
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
            cache = True  
  
        if model is not None:  
            cls._model = model
        return ChatOpenAI(  
            cache=cache,  
            model=cls._model,  
            temperature=0.4,  
            max_tokens=None,  
            timeout=None,  
            max_retries=2,  
            top_p=0.8,  
            api_key=cls._apikey,  
            presence_penalty=0.8,  
            frequency_penalty=0.8,
            base_url="https://api.deepseek.com"
        )  
      
    @classmethod  
    def promptTemplates(cls, input_variable: list = ["answer", "question", "history", "context"]) -> PromptTemplate:  
        return PromptTemplate(  
            input_variables=input_variable,  
            template=cls._template,  
        )  
      
    @classmethod  
    def retrieval(cls, prompt_template: PromptTemplate, model: ChatOpenAI, retriever: VectorStoreRetriever) -> Runnable:  
        prompt = prompt_template  
        if prompt_template == "":  
           prompt = cls.promptTemplates()  
        document_chain = create_stuff_documents_chain(model, prompt) 
        retrieval_chain = create_retrieval_chain(retriever, document_chain)  
        return retrieval_chain  

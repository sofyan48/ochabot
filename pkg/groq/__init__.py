from langchain.globals import set_llm_cache  
from langchain_groq import ChatGroq  
from langchain_redis import RedisCache  
from langchain.chains.combine_documents import create_stuff_documents_chain  
from langchain_core.vectorstores import VectorStoreRetriever  
from langchain_core.prompts import PromptTemplate  
from langchain.chains.retrieval import Runnable, create_retrieval_chain
from pkg.chain.prompter import DefaultPrompter  
  
class GroqLLM:  
    _instance = None    
    _model = "llama-3.3-70b-versatile"    
    _apikey = ""    
    _template = DefaultPrompter.default_prompter()
    
    def __new__(cls, *args, **kwargs):    
        if cls._instance is None:    
            cls._instance = super(GroqLLM, cls).__new__(cls)    
        return cls._instance    
      
    @classmethod  
    def configure(cls, model: str = "llama-3.3-70b-versatile", apikey: str = "", template: str = ""):  
        """Method to configure the model, API key, and template."""  
        cls._model = model if model else cls._model  
        cls._apikey = apikey if apikey else cls._apikey  
        cls._template = template if template else cls._template  
  
    @classmethod  
    def run(cls, redis_url: str = "", model: str = None) -> ChatGroq:  
        cache = False  
        if redis_url != "":  
            redis_cache = RedisCache(redis_url=redis_url, ttl=14400)  
            set_llm_cache(redis_cache)  
            cache = True  
  
        if model is not None:  
            cls._model = model  
              
        return ChatGroq(  
            cache=cache,  
            model_name=cls._model,  
            api_key=cls._apikey,  
            temperature=0.6,  
            n=1,  
        )  
           
    @classmethod  
    def promptTemplates(cls, input_variable: list = ["answer", "question", "history", "context"]) -> PromptTemplate:  
        return PromptTemplate(  
            input_variables=input_variable,  
            template=cls._template,  
        )  
      
    @classmethod  
    def retrieval(cls, prompt_template: PromptTemplate, model: ChatGroq, retriever: VectorStoreRetriever) -> Runnable:  
        prompt = prompt_template  
        if prompt_template == "":  
           prompt = cls.promptTemplates()  
        document_chain = create_stuff_documents_chain(model, prompt)  
        retrieval_chain = create_retrieval_chain(retriever, document_chain)  
        return retrieval_chain  

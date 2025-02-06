from langchain_ollama import OllamaLLM
from langchain.globals import set_llm_cache
from langchain_redis import RedisCache  
from langchain.chains.combine_documents import create_stuff_documents_chain  
from langchain_core.vectorstores import VectorStoreRetriever  
from langchain_core.prompts import PromptTemplate  
from langchain.chains.retrieval import Runnable, create_retrieval_chain  
from pkg.chain.prompter import DefaultPrompter
from pkg.logger.logging import logger

class OllamaPlatform:  
    _instance = None  
    _model = "deepseek-r1:1.5b"  
    _apikey = ""  
    _template = DefaultPrompter.default_prompter()
  
    def __new__(cls, *args, **kwargs):  
        if cls._instance is None:  
            cls._instance = super(OllamaPlatform, cls).__new__(cls)  
        return cls._instance  
  
    @classmethod  
    def configure(cls, model: str = "deepseek-r1:1.5b", apikey: str = "", template: str = ""):  
        if cls._instance is None:  
            cls._instance = super(OllamaPlatform, cls).__new__(cls)  
        cls._model = model if model else cls._model  
        cls._apikey = apikey if apikey else cls._apikey  
        cls._template = template if template else cls._template  
        return cls._instance  

           
    @classmethod  
    def promptTemplates(cls, template="", input_variable: list = ["answer", "question", "history", "context"]) -> PromptTemplate:  
        if template == "":
            template = cls._template
        return PromptTemplate(  
            input_variables=input_variable,  
            template=cls._template,  
        )  

    @classmethod  
    def run(cls, base_url=None, redis_url: str = "", model: str = None, mirostat=2, top_k=4, top_p=0.2) -> OllamaLLM:  
        mirostat_options = {"Mirostat": 1, "Mirostat 2.0": 2}
        mirostat_value = mirostat_options.get(mirostat, 0)
        if mirostat_value == 0:
            mirostat_eta = None
            mirostat_tau = None

        cache = False  
        if redis_url != "":  
            redis_cache = RedisCache(redis_url=redis_url, ttl=14400)  
            set_llm_cache(redis_cache)  
            cache = True  
  
        if model is not None:  
            cls._model = model  
  
        try:
            return OllamaLLM(  
                base_url=base_url,
                cache=cache,  
                model=cls._model, 
                temperature=0.6, 
                top_k=top_k,
                top_p=top_p,
                tfs_z=2.0,
                repeat_last_n=5,
                repeat_penalty=1.1,
                verbose=False,
                # num_gpu=1,
                num_ctx=2048,
                # num_thread=8,
                mirostat_eta=mirostat_eta,
                mirostat_tau=mirostat_tau,
            )  
        except Exception as e:
            logger.error(e)
            raise e

    @classmethod  
    def retrieval(cls, prompt_template: PromptTemplate, model: OllamaLLM, retriever: VectorStoreRetriever) -> Runnable:  
        prompt = prompt_template  
        if prompt_template == "":  
           prompt = cls.promptTemplates()  
        try:
            document_chain = create_stuff_documents_chain(model, prompt) 
        except Exception as e:
            logger.error(e)
            raise e
        
        try:
            return create_retrieval_chain(retriever, document_chain)  
        except Exception as e:
            logger.error(e)
            raise e
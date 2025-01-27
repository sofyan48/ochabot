from langchain_openai.chat_models import ChatOpenAI
from langchain.globals import set_llm_cache
from langchain_redis import RedisCache
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval import Runnable, create_retrieval_chain

class OpenAILLM(object):
    def __init__(self, model:str, apikey:str, template:str):
        if model == "":
            model = "gpt-4o-mini"
        
        self.template = """Your name is Cinbot OpenAI.
        If you don't know, don't go out of context just answer 'I don't know.
        Histroy: {history}
        Context: {context}
        Question: {input}
        Helpfull answer:
        """
        if template != "":
            self.template = template
        self.model = model
        self.apikey = apikey

    def run(self, redis_url="", model=None):
        cache = False
        if redis_url != "":
            redis_cache = RedisCache(redis_url=redis_url, ttl=14400)
            set_llm_cache(redis_cache)
            cache = True

        if model is not None:
            self.model = model
        return ChatOpenAI(
            cache=cache,
            model=self.model,
            temperature=0.4,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            top_p=0.8,
            api_key=self.apikey,
            presence_penalty=0.8,
            frequency_penalty=0.8
        )
    
    def promptTemplates(self, input_variable=["answer", "question", "history", "context"]) -> PromptTemplate:
        return PromptTemplate(
            input_variables=input_variable,
            template=self.template,
        )
    
    def retrieval(self, prompt_template: PromptTemplate, model: ChatOpenAI, retriever: VectorStoreRetriever) -> Runnable:
        prompt = prompt_template
        if prompt_template == "":
           prompt = self.promptTemplates(self.template)
        document_chain = create_stuff_documents_chain(model, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        return retrieval_chain
    

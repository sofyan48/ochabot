
from langchain.globals import set_llm_cache
from langchain_groq import ChatGroq
from langchain_redis import RedisCache
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval import Runnable, create_retrieval_chain


class GroqLLM():
    def __init__(self, model:str, apikey:str, template:str) -> None:
        self.template = """Your name is Cinbot Groq.
        Answer in Bahasa Indonesia.
        If you don't know, don't go out of context just answer 'I don't know.
        Histroy: {history}
        Context: {context}
        Question: {input}
        Helpfull answer:
        """
        if template != "":
            self.template = template
        if model == "":
            model = "llama-3.3-70b-versatile"
        self.model = model
        self.apikey = apikey

    def run(self, redis_url="", model=None) -> ChatGroq:
        cache = False
        if redis_url != "":
            redis_cache = RedisCache(redis_url=redis_url, ttl=14400)
            set_llm_cache(redis_cache)
            cache = False

        if model is not None:
            self.model = model

        return ChatGroq(
            cache=cache,
            model_name=self.model,
            api_key=self.apikey,
            temperature=0.6,
            n=1,
        )
         
    def promptTemplates(self, input_variable=["answer", "question", "history", "context"]) -> PromptTemplate:
        return PromptTemplate(
            input_variables=input_variable,
            template=self.template,
        )
    
    def retrieval(self, prompt_template: PromptTemplate, model: ChatGroq, retriever: VectorStoreRetriever):
        prompt = self.promptTemplates()
        if prompt_template != "":
           prompt = prompt_template
        document_chain = create_stuff_documents_chain(model, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        return retrieval_chain
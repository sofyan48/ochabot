
from langchain.globals import set_llm_cache
from langchain_mistralai.chat_models import ChatMistralAI 
from langchain_redis import RedisCache
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval import Runnable, create_retrieval_chain


class MistralLLM():
    def __init__(self, model:str, apikey:str, template:str) -> None:
        """Your name is Cinbot Mistral.
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
            model = "mistral-large-latest"
        self.model = model
        self.apikey = apikey

    def run(self, redis_url="", model=None) -> ChatMistralAI:
        cache = False
        if redis_url != "":
            redis_cache = RedisCache(redis_url=redis_url, ttl=14400)
            set_llm_cache(redis_cache)
            cache = False

        if model is not None:
            self.model = model
        return ChatMistralAI(
            cache=cache,
            model_name=self.model,
            mistral_api_key=self.apikey,
            temperature=0.6,
            top_k=5,
            top_p=0.8,
            tfs_z=2.0,
        )
         
    def promptTemplates(self, input_variable=["answer", "question", "history", "context"]) -> PromptTemplate:
        return PromptTemplate(
            input_variables=input_variable,
            template=self.template,
        )
    
    def retrieval(self, prompt_template: PromptTemplate, model: ChatMistralAI, retriever: VectorStoreRetriever) -> Runnable:
        prompt = prompt_template
        if prompt_template == "":
           prompt = self.promptTemplates(self.template)
        document_chain = create_stuff_documents_chain(model, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        return retrieval_chain
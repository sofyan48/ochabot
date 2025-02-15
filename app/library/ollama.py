from pkg.ollama import OllamaPlatform, OllamaLLM, Runnable
from pkg.vectorstore.chromadb import VectorStoreRetriever
from app import redis
from app.library.vectorstore import Vectorstores
from pkg.chain import Chain, RunnableWithMessageHistory
from pkg.history import RedisChatMessageHistory, SQLChatMessageHistory
from pkg.chain.prompter import PromptTemplate

class OllamaLibrary(object):
    def __init__(self, vectorstores: Vectorstores, llm: OllamaPlatform, model: str, redis: redis, base_url=None, top_k=4, top_p=0.2):
        self.vectorstores = vectorstores
        self.ollama = llm
        self.model = model
        self.redis = redis
        self.chain = Chain()
        self.top_p = top_p
        self.top_k = top_k
        self.base_url = base_url
    
    def retriever(self, vector, top_k, fetch_k, collection) -> VectorStoreRetriever:
        if top_k is None:
            top_k = 3

        if fetch_k is None:
            fetch_k = 10
        try:
            vectordb = self.vectorstore.configure(vector)
            return vectordb.retriever(
                topK=top_k,
                fetchK=fetch_k,
                collection=collection
            )
        except Exception as e:
            raise e
    
    def get_llm(self, model) -> OllamaLLM:
        try:
            return self.ollama.run(
                base_url=self.base_url,
                top_k = self.top_k,
                top_p=self.top_p,
                redis_url=self.redis.str_conn(),
                model=model
            )
        except Exception as e:
            raise e

    def retrieval(self, promp_tpl: PromptTemplate, retriever: VectorStoreRetriever) -> Runnable:
        llm = self.get_llm(self.model)
        try: 
            return self.ollama.retrieval(
                prompt_template=promp_tpl,
                model=llm,
                retriever=retriever
            )
        except Exception as e:
            raise e
        
    def chain_with_history(
            self, 
            retrival: Runnable, 
            history: RedisChatMessageHistory | SQLChatMessageHistory, 
            input_messages_key: str,
            history_messages_key: str,
            output_messages_key: str
        ) -> RunnableWithMessageHistory:
        
        try:
            return self.chain.chain_with_history(
                retrieval=retrival,
                history=history,
                input_messages_key=input_messages_key,
                history_messages_key=history_messages_key,
                output_messages_key=output_messages_key,
            )
        except Exception as e:
            raise e
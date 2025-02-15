from pkg.groq import GroqLLM, ChatGroq
from pkg.vectorstore.chromadb import VectorStoreRetriever
from app.library.vectorstore import Vectorstores
from app import redis
from pkg.chain import Chain, Runnable
from pkg.runnable import RunnableChain, RunnableWithMessageHistory
from pkg.history import RedisChatMessageHistory
from pkg.chain.prompter import PromptTemplate

class GroqAILibrary(object):
    def __init__(self, vectorstores: Vectorstores, llm: GroqLLM, model: str, redis: redis):
        self.vectorstore = vectorstores
        self.groq = llm
        self.model = model
        self.redis = redis
        self.chain = Chain()
        self.runnable = RunnableChain()
    
    def retriever(self, vector: str, top_k, fetch_k, collection) -> VectorStoreRetriever:
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

    
    def get_llm(self, model) -> ChatGroq:
        try:
            return self.groq.run(
                redis_url=self.redis.str_conn(),
                model=model
            )
        except Exception as e:
            raise e

    def retrieval(self, promp_tpl: PromptTemplate, retriever: VectorStoreRetriever) -> Runnable:
        llm = self.get_llm(self.model)
        try:
            return self.chain.retrieval(
                prompt_template=promp_tpl,
                platform=llm,
                retriever=retriever
            )
        except Exception as e:
            raise e

   
    def chain_with_history(
            self, 
            retrival: Runnable, 
            history: RedisChatMessageHistory, 
            input_messages_key: str,
            history_messages_key: str,
            output_messages_key: str
        ) -> RunnableWithMessageHistory:
        
        try:
            return self.runnable.chain_with_history(
                retrieval=retrival,
                history=history,
                input_messages_key=input_messages_key,
                history_messages_key=history_messages_key,
                output_messages_key=output_messages_key,
            )
        except Exception as e:
            raise e
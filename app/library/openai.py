from pkg.openai import OpenAILLM, Runnable
from pkg.retriever.chroma_retriever import Retriever, VectorStoreRetriever
from app import redis
from pkg.chain import Chain, RunnableWithMessageHistory
from pkg.history import RedisChatMessageHistory, SQLChatMessageHistory
from pkg.chain.prompter import PromptTemplate

class OpenAILibrary(object):
    def __init__(self, chroma: Retriever, llm: OpenAILLM, model: str, redis: redis):
        self.chroma = chroma
        self.openai = llm
        self.model = model
        self.redis = redis
        self.chain = Chain()
    
    def retriever(self, top_k, fetch_k, collection) -> VectorStoreRetriever:
        if top_k is None:
            top_k = 3

        if fetch_k is None:
            fetch_k = 10
        try:
            return self.chroma.retriever(
                topK=top_k,
                fecthK=fetch_k,
                collection=collection
            )
        except Exception as e:
            raise e
    
    def get_llm(self, model):
        try:
            return self.openai.run(
                redis_url=self.redis.str_conn(),
                model=model
            )
        except Exception as e:
            raise e

    def retrieval(self, promp_tpl: PromptTemplate, retriever: VectorStoreRetriever) -> Runnable:
        llm = self.get_llm(self.model)
        try: 
            return self.openai.retrieval(
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
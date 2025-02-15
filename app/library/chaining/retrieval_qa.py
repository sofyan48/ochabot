from pkg.chain import Chain, Runnable
from pkg.runnable import RunnableChain, RunnableWithMessageHistory
from pkg.history import RedisChatMessageHistory, SQLChatMessageHistory
from pkg.chain.prompter import PromptTemplate
from pkg.vectorstore import VectorStoreRetriever
from pkg.chain import Chain

from app.library.platform.mistral import MistralAILibrary
from app.library.platform.openai import OpenAILibrary
from app.library.platform.groq import GroqAILibrary
from app.library.platform.deepseek import DeepSeekLibrary
from app.library.platform.ollama import OllamaLibrary

class RetrievalQAChainLibrary():
    def __init__(self, retriever: VectorStoreRetriever):
        self.chain = Chain()
        self.runnable = RunnableChain()
        self.retriever = retriever

    def retrieval(self, promp_tpl: PromptTemplate, model: None, platform: OpenAILibrary | MistralAILibrary | GroqAILibrary| DeepSeekLibrary| OllamaLibrary) -> Runnable:
        try: 
            platform_running = platform.run(model=model)
            return self.chain.retrieval(
                prompt_template=promp_tpl,
                platform=platform_running,
                retriever=self.retriever
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
            return self.runnable.with_history(
                retrieval=retrival,
                history=history,
                input_messages_key=input_messages_key,
                history_messages_key=history_messages_key,
                output_messages_key=output_messages_key,
            )
        except Exception as e:
            raise e
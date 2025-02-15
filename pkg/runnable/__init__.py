from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.chains.retrieval import Runnable

class RunnableChain(object):
    def __init__(self):
        pass

    def chain_with_history(self, retrieval: Runnable,
            history: RedisChatMessageHistory,
            input_messages_key,
            history_messages_key,
            output_messages_key) -> RunnableWithMessageHistory:
        return RunnableWithMessageHistory(
            retrieval,
            lambda session_id: history,
            input_messages_key=input_messages_key,
            history_messages_key=history_messages_key,
            output_messages_key=output_messages_key
        )
    
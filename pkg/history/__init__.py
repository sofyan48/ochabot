from langchain_community.chat_message_histories import SQLChatMessageHistory, RedisChatMessageHistory

class MessageHistory(object):
    def __init__(self, client=None, session=None) -> SQLChatMessageHistory:
        self.client = client
        self.session = session
        
    def sql(self) -> SQLChatMessageHistory:
        return SQLChatMessageHistory(
            session_id=self.session,
            table_name="messages_history",
            session_id_field_name="session_id",
            connection= self.client,
            async_mode=True
        )
    
    def redis(self, str_conn):
        return RedisChatMessageHistory(
           session_id=self.session,
           url=str_conn,
           ttl=86400
        )
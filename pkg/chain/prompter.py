from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

class DefaultPrompter:
    _instance = None
    _prompter = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DefaultPrompter, cls).__new__(cls)
            cls._prompter = """History:
                {history}
                You are a cinbot,
                Context: {context}
                answer questions according to the context given to you, whatever it is that is important related to the context.
                Question: {input}
                Helpful answer:
            """
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def default_prompter(cls):
        return cls._prompter

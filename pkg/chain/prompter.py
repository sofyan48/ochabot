from langchain_core.prompts import PromptTemplate

class DefaultPrompter:
    _instance = None
    _prompter = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DefaultPrompter, cls).__new__(cls)
            cls._prompter = """Your name is Cinbot.
                Answer in Bahasa Indonesia.
                If you don't know, don't go out of context just answer 'I don't know.
                Histroy: {history}
                Context: {context}
                Question: {input}
                Helpfull answer:
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

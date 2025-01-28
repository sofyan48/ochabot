from langchain_core.prompts import PromptTemplate

class DefaultPrompter(object):
    def __init__(self):
        self.prompter = """Your name is Cinbot OpenAI.
            Answer in Bahasa Indonesia.
            If you don't know, don't go out of context just answer 'I don't know.
            Histroy: {history}
            Context: {context}
            Question: {input}
            Helpfull answer:
        """
    def default_prompter(self):
        return PromptTemplate(template=self.prompter)
    
    def document_prompter(self):
        prompter = """Your name is Cinbot OpenAI.
            Answer in Bahasa Indonesia.
            Histroy: {history}
            Context: {context}
            Question: {input}
            Helpfull answer:
        """
        return PromptTemplate(template=prompter)
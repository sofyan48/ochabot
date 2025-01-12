from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import PromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI


class MistralChainModel():
    def __init__(self, template, path_sqlite="sqlite:///history.db") -> None:
        if template == "":
            template = """Your name is minKA as an AI assistant for kiriminaja.
                Jawab pertanyaan ini menggunakana bahasa indonesia                                 
                Jawab dengan bahasa indonesia yang baik dan benar.
                If you don't know, don't go out of context just answer 'I don't know.
                Histroy: {history}
                Context: {context}
                Question: {input}
                Helpfull answer:"""
        self.template = template
        self.path_sqlite_history = path_sqlite
        
    def promptTemplates(self, input_variable=["answer", "question", "history", "context"]) -> PromptTemplate:
        return PromptTemplate(
            input_variables=input_variable,
            template=self.template,
        )
    
    def retrievalWithMistral(self, prompt_template: str, model: ChatMistralAI, retriever: VectorStoreRetriever):
        prompt = self.promptTemplates(self.template)
        if prompt_template != "":
           prompt = self.promptTemplates(self.template)
        document_chain = create_stuff_documents_chain(model, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        return retrieval_chain

    
        
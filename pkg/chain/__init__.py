from langchain.chains.retrieval import Runnable
from langchain.chains.retrieval import Runnable, create_retrieval_chain  
from langchain_core.vectorstores import VectorStoreRetriever  
from langchain.chains.combine_documents import create_stuff_documents_chain  
from pkg.chain.prompter import DefaultPrompter




class Chain(object):
    def __init__(self):
        self.template = DefaultPrompter.default_prompter()

    def retrieval(self, prompt_template: DefaultPrompter, retriever: VectorStoreRetriever, platform) -> Runnable:  
        prompt = prompt_template  
        if prompt_template == "":  
            prompt = self.template  
        document_chain = create_stuff_documents_chain(platform, prompt) 
        retrieval_chain = create_retrieval_chain(retriever, document_chain)  
        return retrieval_chain  

    
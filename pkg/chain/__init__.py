from langchain.chains.retrieval import Runnable, create_retrieval_chain  
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.vectorstores import VectorStoreRetriever  
from langchain.chains.combine_documents import create_stuff_documents_chain  
from pkg.chain.prompter import DefaultPrompter, PromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.openai_functions.openapi import openapi_spec_to_openai_fn
from langchain_community.utilities.openapi import OpenAPISpec
from pkg.openai import ChatOpenAI
from typing import Any

def _execute_tool(message, call_api_fn) -> Any:
    if tool_calls := message.tool_calls:
        tool_call = tool_calls[0]
        response = call_api_fn(name=tool_call["name"], fn_args=tool_call["args"])
        response.raise_for_status()
        return response.json()
    else:
        return message.content

class Chain(object):
    def __init__(self):
        self.template = DefaultPrompter.default_prompter()

    def retrieval(self, prompt_template: PromptTemplate, retriever: VectorStoreRetriever, platform) -> Runnable:  
        prompt = prompt_template if prompt_template else self.template  
        llm_with_document = create_stuff_documents_chain(platform, prompt) 
        retrieval_chain = create_retrieval_chain(retriever, llm_with_document)  
        return retrieval_chain  
    
    def history_aware_retrieval(self, prompt_template: PromptTemplate, retriever: VectorStoreRetriever, platform):
        prompt = prompt_template if prompt_template else self.template  
        return create_history_aware_retriever(retriever=retriever, prompt=prompt, llm=platform)
    
    def conversation(self, prompt_template: PromptTemplate, platform):
        prompt = prompt_template if prompt_template else self.template  
        return ConversationChain(llm=platform, prompt=prompt)
    
    def open_api_simple_request(self, prompt_template: PromptTemplate, platform: ChatOpenAI, api_spec: str):
        prompt = prompt_template if prompt_template else self.template  
        
        # Parsing the OpenAPI specification
        parsed_spec = OpenAPISpec.from_text(api_spec)
        openai_fns, call_api_fn = openapi_spec_to_openai_fn(parsed_spec)
        
        # Defining tools based on the OpenAPI functions
        tools = [
            {"type": "function", "function": fn}
            for fn in openai_fns
        ]
        
        def execute_tool(message):
            return _execute_tool(message, call_api_fn)
        
        chain = prompt | platform.bind_tools(tools) | execute_tool
        return chain

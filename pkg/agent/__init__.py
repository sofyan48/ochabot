from langchain_community.tools import Tool, tool
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from pkg.openai import ChatOpenAI
from langchain.agents import (
    create_openai_functions_agent,
    AgentExecutor
)


class AgentTools:
    _instance = None
    _tools = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentTools, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def add_tool(cls, tool: Tool):
        """Method to add a tool to the agent tools list."""
        cls._tools.append(tool)
    
    @classmethod
    def list_tools(cls) -> list[Tool]:
        """Method to get the list of tools."""
        return cls._tools
    
    @classmethod
    def get_tool(cls, tool_name: str) -> Tool:
        """Method to select a tool by name."""
        for tool in cls._tools:
            if not hasattr(tool, "name"):
                raise AttributeError(f"Tool object {tool} does not have a 'name' attribute.")
            if tool.name == tool_name:
                return tool
        raise ValueError(f"Tool with name '{tool_name}' not found.")

    @classmethod
    def agent_functions(cls, llm: ChatOpenAI, tools: list, model: str, prompt: PromptTemplate = "You are a helpful assistant that can use tools to answer questions.") -> Runnable:
        return create_openai_functions_agent(
            llm=llm,
            tools=tools,
            prompt= prompt
        )

    @classmethod
    def executor(cls, agent: Runnable, tools: list = [], verbose: bool = False, return_intermediate_steps: bool = True) -> Runnable:
        """Method to create an agent executor."""
        return AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=verbose,
            return_intermediate_steps=return_intermediate_steps
        )


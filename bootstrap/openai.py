from pkg.openai import OpenAILLM, OpenAIDirect
from pkg.chain.prompter import DefaultPrompter
import os

def register_openai() -> OpenAILLM:
    template = DefaultPrompter.default_prompter()
    return OpenAILLM().configure(
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
        apikey=os.getenv("OPENAI_APIKEY", "OPENAI_APIKEY"),
        template=template
    )

def register_openai_direct() -> OpenAILLM:
    return OpenAIDirect().configure(
        apikey=os.getenv("OPENAI_APIKEY", "OPENAI_APIKEY"),
    )
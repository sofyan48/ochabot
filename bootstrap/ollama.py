from pkg.ollama import OllamaPlatform
from pkg.chain.prompter import DefaultPrompter
import os

def register_ollama():
    template = DefaultPrompter.default_prompter()
    return OllamaPlatform().configure(
        model=os.getenv("OLLAMA_MODEL","deepseek-r1:1.5b"),
        apikey=os.getenv("OLLAMA_APIKEY", "OLLAMA_APIKEY"),
        template= template
    )
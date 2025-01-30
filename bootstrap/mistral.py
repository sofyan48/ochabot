from pkg.mistral import MistralLLM
from pkg.chain.prompter import DefaultPrompter
import os

def register_mistral():
    template = DefaultPrompter.default_prompter()
    return MistralLLM().configure(
        model=os.getenv("MISTRAL_BASE","open-mistral-nemo"),
        apikey=os.getenv("MISTRAL_API_KEY", "MISTRAL_API_KEY"),
        template= template
    )
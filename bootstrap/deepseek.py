from pkg.deepseek import DeepSeekLLM
from pkg.chain.prompter import DefaultPrompter
import os

def register_deepseek() -> DeepSeekLLM:
    template = DefaultPrompter.default_prompter()
    return DeepSeekLLM().configure(
        model=os.getenv("DEEPSEEK_MODEL","gpt-4o-mini"),
        apikey=os.getenv("DEEPSEEK_APIKEY", "OPENAI_APIKEY"),
        template=template
    )

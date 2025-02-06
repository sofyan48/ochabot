from pkg.deepseek import DeepSeekLLM
from pkg.chain.prompter import DefaultPrompter
import os

def register_deepseek() -> DeepSeekLLM:
    template = DefaultPrompter.default_prompter()
    return DeepSeekLLM().configure(
        
        template=template
    )

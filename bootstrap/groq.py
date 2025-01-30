from pkg.groq import GroqLLM
from pkg.chain.prompter import DefaultPrompter
import os

def register_groq():
    template = DefaultPrompter.default_prompter()
    return GroqLLM().configure(
        model=os.getenv("GROQ_BASE","llama-3.3-70b-versatile"),
        apikey=os.getenv("GROQ_APIKEY", "GROQ_APIKEY"),
        template= template
    )
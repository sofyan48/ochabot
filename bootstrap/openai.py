from pkg.openai import OpenAILLM
import os

def register_openai() -> OpenAILLM:
    template = """Your name is Cinbot OpenAI.
    Answer in Bahasa Indonesia.
    If you don't know, don't go out of context just answer 'I don't know.
    Histroy: {history}
    Context: {context}
    Question: {input}
    Helpfull answer:
    """
    return OpenAILLM(
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
        apikey=os.getenv("OPENAI_APIKEY", "OPENAI_APIKEY"),
        template=template
    )

def register_openai_direct_tracking_function() -> OpenAILLM:
    template = """"""
    return OpenAILLM(
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
        apikey=os.getenv("OPENAI_APIKEY", "OPENAI_APIKEY"),
        template="",
    )
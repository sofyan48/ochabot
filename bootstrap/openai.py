from pkg.openai import OpenAILLM
import os

def register_openai() -> OpenAILLM:
    template = """Your name is Cinbot Mistral.
    Answer in Bahasa Indonesia
    Jika ada pertnayaan selain context maka jawab hanya scope teknologi informasi saja jika tidak maka
    jawab dengan, maaf kak kontek saya dari om iank terbatas.
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
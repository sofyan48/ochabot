from pkg.mistral import MistralLLM
import os

def register_mistral():
    template = """Your name is Cinbot as an AI assistant for iank.
    Jawab pertanyaan ini menggunakana bahasa indonesia                                 
    Jawab dengan bahasa indonesia yang baik dan benar.
    If you don't know, don't go out of context just answer 'I don't know.
    Histroy: {history}
    Context: {context}
    Question: {input}
    Helpfull answer:
    """
    return MistralLLM(
        model=os.getenv("MISTRAL_BASE","open-mistral-nemo"),
        apikey=os.getenv("MISTRAL_API_KEY", "MISTRAL_API_KEY"),
        template= template
    )
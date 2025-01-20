from pkg.groq import GroqLLM
import os

def register_groq():
    template = """Your name is Cinbot as an AI assistant for iank.
    Jawab pertanyaan ini menggunakana bahasa indonesia                                 
    Jawab dengan bahasa indonesia yang baik dan benar.
    If you don't know, don't go out of context just answer 'I don't know.
    Histroy: {history}
    Context: {context}
    Question: {input}
    Helpfull answer:
    """
    return GroqLLM(
        model=os.getenv("GROQ_BASE","llama-3.3-70b-versatile"),
        apikey=os.getenv("GROQ_APIKEY", "GROQ_APIKEY"),
        template= template
    )
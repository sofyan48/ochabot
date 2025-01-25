from pkg.groq import GroqLLM
import os

def register_groq():
    template = """Your name is Cinbot Mistral.
    Answer in Bahasa Indonesia
    utamakan context om iank,
    Jika ada pertanyaan selain context maka jawab hanya terkait teknologi saja.
    jika pertanya selain om iank dan teknologi maka jawab saya tidak tau kak
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
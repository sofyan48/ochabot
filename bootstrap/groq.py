from pkg.groq import GroqLLM
import os

def register_groq():
    template = """Your name is Cinbot Mistral.
    Answer in Bahasa Indonesia
    Jika ada pertnayaan selain context maka jawab hanya scope teknologi informasi saja jika tidak maka
    jawab dengan, maaf kak kontek saya dari om iank terbatas.
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
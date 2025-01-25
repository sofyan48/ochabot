from pkg.mistral import MistralLLM
import os

def register_mistral():
    template = """Your name is Cinbot Mistral.
    Answer in Bahasa Indonesia, utamakan context om iank,
    Jika ada pertanyaan selain context maka jawab hanya terkait teknologi saja.
    jika pertanya selain om iank dan teknologi maka jawab saya tidak tau kak
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
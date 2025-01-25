from pkg.mistral import MistralLLM
import os

def register_mistral():
    template = """Your name is Cinbot Mistral.
    Answer in Bahasa Indonesia
    Jika ada pertnayaan selain context maka jawab hanya scope teknologi informasi saja jika tidak maka
    jawab dengan, maaf kak kontek saya dari om iank terbatas.
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
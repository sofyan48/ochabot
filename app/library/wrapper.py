from app.library.mistral import MistralAILibrary
from app.library.openai import OpenAILibrary
from app.library.groq import GroqAILibrary
from app import (
                llm_openai, 
                llm_mistral,
                llm_qroq,
                chromadb,
                redis
            )

class AIWrapperLLM(object):
    def __init__(self, model="openai"):
        self.model = self.openai()
        if model == "mistral":
            self.model = self.mistral()
        

    def mistral(self):
        return MistralAILibrary(
            chroma=chromadb,
            llm=llm_mistral,
            redis=redis
        )
    def openai(self):
        return OpenAILibrary(
            chroma=chromadb,
            llm=llm_openai,
            redis=redis
        )
    
    def groq(self):
        return GroqAILibrary(
            chroma=chromadb,
            llm=llm_qroq,
            redis=redis
        )
    
    def initiate(self, model: str = "openai") -> (OpenAILibrary | MistralAILibrary):
        self.model = self.openai()
        if model == "mistral":
            self.model = self.mistral()
        elif model == "groq":
            self.model = self.groq()
        return self.model
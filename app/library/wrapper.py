from app.library.mistral import MistralAILibrary
from app.library.openai import OpenAILibrary
from app.library.groq import GroqAILibrary
from app.library.deepseek import DeepSeekLibrary
from app import (
                redis,
                logger
            )

from app.library import (
    mistral_llm, 
    openai_llm, 
    groq_llm, 
    chromadb,
    deepseek_llm
)

class AIWrapperLLM(object):
    def __init__(self, llm="mistral", model="open-mistral-nemo"):
        if llm == "openai":
            self.llm = self.openai(model="gpt-4o-mini")
        elif llm == "groq":
            self.llm = self.groq(model="llama-3.3-70b-versatile")
        elif llm == "deepseek":
            self.llm = self.deepseek(model="deepseek-chat")
        else:
            self.llm = self.mistral(model=model)
        
        self.model = model
        self.llm_name = llm

    def mistral(self, model=None):
        if model is None:
            model = "open-mistral-nemo"
        return MistralAILibrary(
            chroma=chromadb,
            llm=mistral_llm,
            redis=redis,
            model=model
        )
    
    def openai(self, model=None):
        if model is None:
            model = "gpt-4o-mini"
        return OpenAILibrary(
            chroma=chromadb,
            llm=openai_llm,
            redis=redis,
            model=model
        )
    
    def groq(self, model="llama-3.3-70b-versatile"):
        if model is None:
            model = "llama-3.3-70b-versatile"
        return GroqAILibrary(
            chroma=chromadb,
            llm=groq_llm,
            redis=redis,
            model=model
        )
    
    def deepseek(self, model=None):
        if model is None:
            model = "deepseek-chat"
        return DeepSeekLibrary(
            chroma=chromadb,
            llm=deepseek_llm,
            redis=redis,
            model=model
        )
    
    def initiate(self, llm: str = "mistral", model=None) -> (OpenAILibrary | MistralAILibrary | GroqAILibrary| DeepSeekLibrary):
        if model is None:
            model = None
        if llm == "mistral":
            return self.mistral(model=model)
        if llm == "openai":
            return  self.openai(model=model)  
        elif llm == "groq":
            return  self.groq(model=model)
        elif llm == "deepseek":
            return  self.deepseek(model=model)
        else:
            return self.llm
            
        
        
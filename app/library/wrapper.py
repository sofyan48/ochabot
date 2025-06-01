from app.library.platform.mistral import MistralAILibrary
from app.library.platform.openai import OpenAILibrary
from app.library.platform.groq import GroqAILibrary
from app.library.platform.deepseek import DeepSeekLibrary
from app.library.platform.ollama import OllamaLibrary
from app import (
                redis,
                logger
            )

from app.library import (
    mistral_llm, 
    openai_llm, 
    groq_llm, 
    deepseek_llm,
    ollama_llm
)

class AIWrapperLLM(object):
    def __init__(self, llm="mistral", model="open-mistral-nemo"):
        if llm == "openai":
            self.llm = self.openai(model="gpt-4o-mini")
        elif llm == "groq":
            self.llm = self.groq(model="llama-3.3-70b-versatile")
        elif llm == "deepseek":
            self.llm = self.deepseek(model="deepseek-chat")
        elif llm == "ollama":
            self.llm = self.ollama(model="deepseek-r1:1.5b")
        else:
            self.llm = self.mistral(model=model)
        self.model = model
        self.llm_name = llm

    def mistral(self, model=None):
        if model is None:
            model = "open-mistral-nemo"
        try:
            return MistralAILibrary(
                llm=mistral_llm,
                redis=redis,
                model=model
            )
        except Exception as e:
            raise e
    
    def openai(self, model=None):
        if model is None:
            model = "gpt-4o-mini"
        
        try:
            return OpenAILibrary(
                llm=openai_llm,
                redis=redis,
                model=model
            )
        except Exception as e:
            raise e
    
    def groq(self, model="llama-3.3-70b-versatile"):
        if model is None:
            model = "llama-3.3-70b-versatile"
        try:
            return GroqAILibrary(
                llm=groq_llm,
                redis=redis,
                model=model
            )
        except Exception as e:
            raise e
    
    def deepseek(self, model=None):
        if model is None:
            model = "deepseek-chat"
        try:
            return DeepSeekLibrary(
                llm=deepseek_llm,
                redis=redis,
                model=model
            )
        except Exception as e:
            raise e
    
    def ollama(self, model=None):
        if model is None:
            model = "deepseek-r1:1.5b"
        try:
            return OllamaLibrary(
                llm=ollama_llm,
                redis=redis,
                model=model,
            )
        except Exception as e:
            raise e
    
    def initiate(self, llm: str = "mistral", model=None) -> (OpenAILibrary | MistralAILibrary | GroqAILibrary| DeepSeekLibrary| OllamaLibrary):
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
        elif llm == "ollama":
            return  self.ollama(model=model)
        else:
            return self.llm
            
        
        
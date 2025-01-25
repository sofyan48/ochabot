from app.library.mistral import MistralAILibrary
from app.library.openai import OpenAILibrary
from app.library.groq import GroqAILibrary
from app import (
                llm_openai, 
                llm_mistral,
                llm_qroq,
                chromadb,
                redis,
                logger
            )

class AIWrapperLLM(object):
    def __init__(self, llm="mistral", model="open-mistral-nemo"):
        if llm == "openai":
            self.llm = self.openai(model="gpt-4o-mini")
        elif llm == "groq":
            self.llm = self.groq(model="llama-3.3-70b-versatile")
        else:
            self.llm = self.mistral(model=model)
        
        self.model = model
        self.llm_name = llm

    def mistral(self, model=None):
        if model is None:
            model = "open-mistral-nemo"
        return MistralAILibrary(
            chroma=chromadb,
            llm=llm_mistral,
            redis=redis,
            model=model
        )
    def openai(self, model=None):

        if model is None:
            model = "gpt-4o-mini"
        return OpenAILibrary(
            chroma=chromadb,
            llm=llm_openai,
            redis=redis,
            model=model
        )
    
    def groq(self, model="llama-3.3-70b-versatile"):
        if model is None:
            model = "llama-3.3-70b-versatile"
        return GroqAILibrary(
            chroma=chromadb,
            llm=llm_qroq,
            redis=redis,
            model=model
        )
    
    def initiate(self, llm: str = "mistral", model=None) -> (OpenAILibrary | MistralAILibrary | GroqAILibrary):
        print(llm, model)
        if model is None:
            logger.info("Using default setup model", {
                "model": self.model,
                "llm": self.llm_name
            })
        if llm == "mistral":
            return self.mistral(model=model)
        if llm == "openai":
            return  self.openai(model=model)  
        elif llm == "groq":
            return  self.groq(model=model)
        else:
            return self.llm
            
        
        
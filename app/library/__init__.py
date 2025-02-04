from app import (
                redis,
                logger
            )
from pkg.mistral import MistralLLM
from pkg.openai import OpenAILLM
from pkg.groq import GroqLLM
from pkg.vectorstore.chromadb import ChromaDB
from pkg.storage.minio import StorageMinio

mistral_llm = MistralLLM()
openai_llm = OpenAILLM()
groq_llm = GroqLLM()
chromadb = ChromaDB()
minio = StorageMinio

from app.repositories.setup import SetupConfig
from app.repositories.prompt import PromptRepositories
repo_config = SetupConfig()
repo_prompt = PromptRepositories()
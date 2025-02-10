from app import (
                redis,
            )
from pkg.mistral import MistralLLM
from pkg.openai import OpenAILLM
from pkg.groq import GroqLLM
from pkg.vectorstore.chromadb import ChromaDB
from pkg.storage.minio import StorageMinio
from pkg.deepseek import DeepSeekLLM
from pkg.ollama import OllamaPlatform
from pkg.vectorstore.elasticsearch import ElasticsearcVector
from app.library.vectorstore import Vectorstores

from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:chat")

mistral_llm = MistralLLM()
openai_llm = OpenAILLM()
groq_llm = GroqLLM()
deepseek_llm = DeepSeekLLM()
ollama_llm = OllamaPlatform()
chromadb = ChromaDB()
elastic = ElasticsearcVector
minio = StorageMinio
vectorstoreDB = Vectorstores()


from app.repositories.setup import SetupConfig
from app.repositories.prompt import PromptRepositories
repo_config = SetupConfig()
repo_prompt = PromptRepositories()
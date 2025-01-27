from pydantic import BaseModel, Field
from typing import Optional


class RequesChat(BaseModel):
    chat: str = Field(..., min_length=1)
    collection: Optional[str] = None
    llm: Optional[str] = None
    model: Optional[str] = None


class RequestPrompt(BaseModel):
    prompt: str = Field(..., min_length=1)

class RequestLLMSetup(BaseModel):
    platform: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)

class RequestRetrievalSetup(BaseModel):
    top_k: int = Field(...)
    fetch_k: int = Field(...)
    overlap: int = Field(...)
    collection: str = Field(...)
    vector_db: str = Field(...)

class RequestDeleteSetup(BaseModel):
    key: str = Field(..., min_length=1)
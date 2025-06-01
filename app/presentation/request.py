from pydantic import BaseModel, Field
from typing import Optional


class RequesChat(BaseModel):
    chat: str = Field(..., min_length=1)
    scope_id: int = Field(...)
    llm: Optional[str] = None
    model: Optional[str] = None
    input_variabels: Optional[list] = None

class RequesChatAgent(BaseModel):
    chat: str = Field(..., min_length=1)
    agent: Optional[str] = None
    llm: Optional[str] = None
    model: Optional[str] = None
    


class RequestPrompt(BaseModel):
    id: Optional[int] = None
    prompt: str = Field(..., min_length=1)
    scope_id: int = Field(..., ge=1)
    is_default: Optional[bool] = False

class RequestScopePrompt(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1)

class RequestLLMSetup(BaseModel):
    platform: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)

class RequestRetrievalSetup(BaseModel):
    top_k: int = Field(...)
    fetch_k: int = Field(...)
    overlap: int = Field(...)
    vector_db: str = Field(...)

class RequestDeleteSetup(BaseModel):
    key: str = Field(..., min_length=1)

class RequestClientSocket(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1)

class RequestUsers(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    is_active: Optional[bool] = True

class RequestClient(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1)
    is_active: Optional[bool] = True

class RequestLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class RequestGrantClient(BaseModel):
    api_key: str = Field(..., min_length=1)
    secret_key: str = Field(..., min_length=1)

class RequestIngestVector(BaseModel):
    scope_id: int = Field(...)
    ingest_code: str = Field(..., min_length=1)

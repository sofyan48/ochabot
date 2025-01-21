from pydantic import BaseModel, Field
from typing import Optional


class RequesChat(BaseModel):
    chat: str = Field(..., min_length=1)
    collection: str = Field(..., min_length=1)
    llm: Optional[str] = None
    model: Optional[str] = None



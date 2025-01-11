from pydantic import BaseModel, constr
from typing import Any, Dict


class RequesChat(BaseModel):
    chat: constr(min_length=1)
    collection: constr(min_length=1)

class RequestDatasheet(BaseModel):
    question: constr(min_length=5)
    answer: constr(min_length=5)

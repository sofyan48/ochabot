from math import ceil
from typing import Any, Generic, TypeVar
from collections.abc import Sequence
from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic import Field
from pydantic import BaseModel as GenericModel

DataType = TypeVar("DataType")
T = TypeVar("T")


class IResponseBase(GenericModel, Generic[T]):
    message: str = ""
    meta: dict = {}
    data: T | None

def response(
    data: DataType,
    message: str | None = None,
    meta: dict | Any | None = {}) -> (IResponseBase[DataType]):
    response = {}
    if message is not None:
        response["message"] = message
    if data is not None:
        response["data"] = data
    if meta is not None:
        response["meta"] = meta
    return response
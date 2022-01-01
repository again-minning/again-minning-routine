from typing import Generic, TypeVar, Optional

from pydantic import BaseModel
from pydantic.generics import GenericModel
from base.utils.constants import HttpStatus

DataT = TypeVar('DataT')


class Message(BaseModel):
    status: HttpStatus
    msg: str


class Response(GenericModel, Generic[DataT]):
    message: Message
    data: Optional[DataT]

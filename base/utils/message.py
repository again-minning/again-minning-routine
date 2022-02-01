from typing import Generic, TypeVar, Optional

from pydantic import BaseModel
from pydantic.generics import GenericModel

from base.utils.constants import HttpStatus

T = TypeVar('T')
E = TypeVar('E')


class Message(BaseModel):
    status: HttpStatus = HttpStatus.OK
    msg: str = 'success'


class Response(GenericModel, Generic[E, T]):
    message: Optional[E]
    data: Optional[T]

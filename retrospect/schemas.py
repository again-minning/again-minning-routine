from pydantic import BaseModel


class RetrospectCoreBase(BaseModel):
    content: str


class RetrospectCreateResponse(RetrospectCoreBase):
    pass


class Retrospect(BaseModel):
    pass

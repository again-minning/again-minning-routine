from pydantic import BaseModel


class SimpleSuccessResponse(BaseModel):
    success: bool

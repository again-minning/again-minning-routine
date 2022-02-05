from pydantic import BaseModel


class RetrospectResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    url: str

    @classmethod
    def to_response(cls, retrospect):
        return RetrospectResponseSchema(
            id=retrospect.id,
            title=retrospect.title,
            content=retrospect.content,
            url=retrospect.image.url if retrospect.image else ''
        )

    @classmethod
    def to_list_response(cls, retrospects):
        result = []
        for retrospect in retrospects:
            result.append(RetrospectResponseSchema.to_response(retrospect))
        return result

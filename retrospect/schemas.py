from pydantic import BaseModel


class DetailRetrospectSchema(BaseModel):
    id: int
    title: str
    content: str
    url: str

    @classmethod
    def to_response(cls, retrospect):
        return DetailRetrospectSchema(
            id=retrospect.id,
            title=retrospect.title,
            content=retrospect.content,
            url=retrospect.image.url if retrospect.image else ''
        )

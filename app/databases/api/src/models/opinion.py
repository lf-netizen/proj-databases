import nanoid
from pydantic import BaseModel, Field


class Opinion(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    user_id: int
    product_id: str
    content: str


class OpinionUpdate(BaseModel):
    user_id: int | None = None
    product_id: str | None = None
    content: str | None = None

from datetime import datetime
from pydantic import BaseModel, Field
class ParsedMessage(BaseModel):
    url: str = Field()
    date: datetime = Field()
    author: str = Field()
    body: str = Field()
    title: str = Field()
    links: list[str] | None = Field()
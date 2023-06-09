from datetime import datetime
from pydantic import BaseModel, Field

class ParsedMessage(BaseModel):
    url: str = Field()
    date: datetime = Field()
    author: list[str] = Field()
    body: str = Field()
    title: str = Field()
    links: list[str] | None = Field()
    status: str = Field(default="")
from datetime import datetime
from abc import ABC

from objects.schemas import ParsedMessage

class IParser(ABC):
    @classmethod
    def _get_author(cls, html: str) -> list[str]:
        ...

    @classmethod
    def _get_date(cls, html: str) -> datetime:
        ...

    @classmethod
    def _get_body(cls, html: str) -> str:
        ...

    @classmethod
    def _get_title(cls, html: str) -> str:
        ...

    @classmethod
    def _get_url(cls, html: str) -> str:
        ...
    @classmethod
    def _get_links(cls, html: str) -> list[str] | None:
        ...
    @classmethod
    def parse(cls, html: str) -> ParsedMessage:
        return ParsedMessage(
            url=cls._get_url(html=html),
            date=cls._get_date(html=html),
            author=cls._get_author(html=html),
            body=cls._get_body(html=html),
            title=cls._get_title(html=html),
            links=cls._get_links(html=html),
        )

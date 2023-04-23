from datetime import datetime
from bs4 import BeautifulSoup

from objects.IEntities import IParser


class RbcParser(IParser):
    @classmethod
    def _get_author(cls, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        author_span = soup.find('span', class_='article__authors__author__name')
        return author_span.text

    @classmethod
    def _get_date(cls, html: str) -> datetime:
        soup = BeautifulSoup(html, 'html.parser')
        time_tag = soup.find('time', class_='article__header__date')
        time = time_tag['datetime']
        return datetime.fromisoformat(time)

    @classmethod
    def _get_body(cls, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        body_div = soup.find('div', class_='article__text article__text_free')
        paragraphs = body_div.find_all(name='p')
        body = []
        for p in paragraphs:
            if len(p.find_all()) == 0:
                body.append(p.text)
        body_text = '\n'.join(body)
        return body_text

    @classmethod
    def _get_title(cls, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string.replace(' — РБК', '')
        return title

    @classmethod
    def _get_links(cls, html: str) -> list[str] | None:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        links_ = soup.find_all('a')
        for link in links_:
            link_url = link.get('href')
            if link_url and link_url.startswith('https://www.rbc.ru/') and 'from' in link_url:
                links.append(link_url)
        return links

    @classmethod
    def _get_url(cls, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        meta_tag = soup.find('meta', property='og:url')
        url = meta_tag['content']
        return url
import requests
from bs4 import BeautifulSoup

res = requests.get('https://www.rbc.ru/politics/06/04/2023/642ee4d29a7947600b911714')

with open('rbc_test.html', 'w') as file:
    file.write(res.text)

soup = BeautifulSoup(res.text, 'html.parser')

author_span = soup.find('span', class_='article__authors__author__name')
author = author_span.text

time_tag = soup.find('time', class_='article__header__date')
time = time_tag['datetime']

title = soup.title.string.replace(' — РБК', '')

body_div = soup.find('div', class_='article__text article__text_free')


paragraphs = body_div.find_all(name='p')
body = []
for p in paragraphs:
    if len(p.find_all()) == 0:
        body.append(p.text)
body_text = '\n'.join(body)

links = []
links_ = soup.find_all('a')
for link in links_:
    link_url = link.get('href')
    if link_url and link_url.startswith('https://www.rbc.ru/') and 'from' in link_url:
        links.append(link_url)

meta_tag = soup.find('meta', property='og:url')
url = meta_tag['content']
print(url)

# print(author)
# print(time)
# print(title)
# print(links)
with open('body_test.txt', 'w') as file:
    file.write(body_text)

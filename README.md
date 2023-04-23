# Техническое описание используемого стека технологий:
1. Работа с RMQ: [pika](https://pika.readthedocs.io/en/stable/), [aio-pika](https://aio-pika.readthedocs.io/en/latest/)
2. Сетевое взаимодействие с таргетным Интернет-ресурсом: [aiohttp](https://docs.aiohttp.org/en/stable/)

# Запуск:
1. Сборка образа: `docker-compose build`
2. Запуск контейнеров: `docker-compose up -d`
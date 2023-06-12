# Техническое описание используемого стека технологий:
1. Работа с RMQ: [pika](https://pika.readthedocs.io/en/stable/), [aio-pika](https://aio-pika.readthedocs.io/en/latest/)
2. Сетевое взаимодействие с таргетным Интернет-ресурсом: [aiohttp](https://docs.aiohttp.org/en/stable/)

# Запуск:
1. Сборка образа: `docker-compose build`
2. Запуск контейнеров: `docker-compose up -d`

# Визулизация:
В папке `dashboards` имеются примеры агрегаций

# Анализ текстов:
Для анализа тональности текстов была использована библиотека [dostoevsky](https://pypi.org/project/dostoevsky/) и обученая на наборе [rusentiment
](https://github.com/text-machine-lab/rusentiment) модель fasttext-social-network-model

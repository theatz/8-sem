FROM python:3.10

ENV TZ="Europe/Moscow"

ARG APP_DIR=/src
ARG PY_VERSION=3.10

RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}
ADD /src ${APP_DIR}
ADD requirements.txt .

RUN pip3 install -r requirements.txt
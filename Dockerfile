FROM python:3.9.5-slim-buster

LABEL maintainer="shoytov@gmail.com"
LABEL vendor="Dmitry Shoytov"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONHASHSEED=random
ENV POETRY_VERSION=1.1.13
ENV PYTHONPATH=${PYTHONPATH}:/

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install "poetry>=$POETRY_VERSION" \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

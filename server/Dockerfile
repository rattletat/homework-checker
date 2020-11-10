FROM python:3.8.5-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED=random

ENV POETRY_VERSION=1.0.10
ENV POETRY_VIRTUALENVS_CREATE=false

ENV DJANGO_READ_ENV_FILE=true
ENV DJANGO_SETTINGS_MODULE="config.settings.dev"

# System dependencies
RUN apt-get update \
  && apt-get -y install gcc postgresql \
  && apt-get clean

# Python dependencies
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry install --no-interaction --no-ansi

# Entrypoint
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/
COPY .env.dev /usr/src/app/.env

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


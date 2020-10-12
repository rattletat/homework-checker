FROM python:3.8.2-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=1.0.10
ENV POETRY_VIRTUALENVS_CREATE=false

ENV DJANGO_SETTINGS_MODULE="config.settings.dev"

# System dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

# Python dependencies
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /usr/src/app/

# TODO: Add --no-dev if DEBUG=True
RUN poetry install --no-interaction --no-ansi

# Entrypoint
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


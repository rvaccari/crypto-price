FROM python:3.9-slim

#
# CONTAINER CONFIGURATION
#
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

WORKDIR /app
RUN pip install --progress-bar off -U pip setuptools && \
    hash poetry >/dev/null 2>&1 || pip install --progress-bar off poetry
RUN poetry config virtualenvs.create false

#
# INSTALL APP and DEPENDENCIES
#
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-ansi --no-root

COPY . /app/
RUN python contrib/env_gen.py

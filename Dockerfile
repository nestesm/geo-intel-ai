FROM python:3.11.5-slim-bookworm AS base
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git build-essential \
    && apt-get autoremove -y

FROM base AS install
WORKDIR /opt

COPY requirements.txt .

# install without virtualenv, since we are inside a container
RUN pip install -r requirements.txt

RUN apt-get purge -y curl git build-essential \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

FROM install as app-image

COPY . .

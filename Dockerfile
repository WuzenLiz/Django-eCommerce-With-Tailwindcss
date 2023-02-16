# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DockerHome=/app \
    PORT=8000 \
    NODE_VERSION=18.14.0

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    binutils \
    libproj-dev \
    gdal-bin \
    postgis \
 && rm -rf /var/lib/apt/lists/*

# # Install the application server.
# RUN pip install "gunicorn==20.0.4"

# Install nodejs
## get nodejs version manager (nvm)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

## install nodejs
RUN . ~/.nvm/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

## set nodejs as default
RUN ln -s ~/.nvm/versions/node/v$NODE_VERSION/bin/node /usr/local/bin/node

## set npm as default
RUN ln -s ~/.nvm/versions/node/v$NODE_VERSION/bin/npm /usr/local/bin/npm

## set npx as default
RUN ln -s ~/.nvm/versions/node/v$NODE_VERSION/bin/npx /usr/local/bin/npx

## set yarn as default
RUN ln -s ~/.nvm/versions/node/v$NODE_VERSION/bin/yarn /usr/local/bin/yarn

# Install node packages
RUN npm install -g npm@latest

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY package.json /
COPY package-lock.json /

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy the source code of the project into the container.
COPY . .



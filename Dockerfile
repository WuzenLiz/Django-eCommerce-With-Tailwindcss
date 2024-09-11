# Use an official Python runtime based on "bullseye" as a parent image.
FROM python:3.12.5-slim-bullseye

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
    libmariadb-dev-compat \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    binutils \
    libproj-dev \
    gdal-bin \
    gettext \
    gettext-base \
    && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# # Install the application server.
# RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY package.json /
COPY package-lock.json /

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy the source code of the project into the container.
COPY . .



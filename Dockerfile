# ---------------------------------- WARNING ----------------------------------
# This file is primarily for production use with k8s
# See Dockerfile in subdirectories for dev use with docker-compose
# ---------------------------------- WARNING ----------------------------------

# ---
# build scss in separate image
# ---
FROM node:18-alpine as sass-compile

WORKDIR /app

COPY ./sass-compile/package.json ./sass-compile/package-lock.json ./
RUN npm ci

COPY ./sass-compile/scss ./scss

RUN npm run css

# ---
# wagtail image
# ---
FROM python:3.11.5-slim-bookworm

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Add contrib repository to apt sources
RUN sed -i "s/ main/ main contrib/g" /etc/apt/sources.list.d/debian.sources

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    gettext -y \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    libmagickwand-dev \
    wkhtmltopdf \
    xfonts-75dpi \
    xfonts-base \
    ttf-mscorefonts-installer \
    xauth \
    xvfb \
 && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf from deb package (patched version)
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6.1-3.bookworm_amd64.deb
RUN rm wkhtmltox_0.12.6.1-3.bookworm_amd64.deb

# Install the application server.
RUN pip install "gunicorn==21.2.0"

# Install the project requirements.
COPY ./rog/requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail ./rog .

# Copy compiled css from other image
COPY --chown=wagtail:wagtail --from=sass-compile /app/static/css ./rog/static/css

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

CMD gunicorn rog.wsgi:application -b 0.0.0.0:8000 --log-level DEBUG

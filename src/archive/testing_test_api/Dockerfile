# Use the official Debian-hosted Python image
FROM python:3.8.12-slim-buster

# JZ: update credential
ENV GOOGLE_APPLICATION_CREDENTIALS=../../../secrets/ccb.json

# Ensure we have an up to date baseline, install dependencies 
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libsndfile1 \
        vim && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    mkdir -p /app

WORKDIR /app

# Add Pipfile, Pipfile.lock
ADD Pipfile Pipfile.lock /app/

# check to sync
RUN pipenv sync

# Source code
ADD . /app

# Run script (avoid creating shell)
ENTRYPOINT ["pipenv", "run"]
CMD ["python", "testing_test_api.py"]

# Use docker run -it <image_name> /bin/bash to create interactive session for development

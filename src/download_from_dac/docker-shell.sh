#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/secrets/

# Create the network if we don't have it yet
docker network inspect ccb-preprocessing-network >/dev/null 2>&1 || docker network create ccb-preprocessing-network

# Build the image based on the Dockerfile
docker build -t preprocessing .

# Run Container
docker run --rm --name ccb-preprocessing -ti --entrypoint /bin/bash \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v ~/.gitconfig:/etc/gitconfig \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ccb.json
--network ccb-preprocessing-network preprocessing
#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/

# Create the network if we don't have it yet
docker network inspect ccb-test_api-network >/dev/null 2>&1 || docker network create ccb-test_api-network

# Build the image based on the Dockerfile
docker build -t test_api .

# Run Container - run entrypoint/cmd automatically
docker run --rm --name ccb-test_api -ti --entrypoint /bin/bash \
-p 8000:8000 \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/../../../secrets \
-v ~/.gitconfig:/etc/gitconfig \
-e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
--network ccb-test_api-network test_api
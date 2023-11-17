#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/

# Build the image based on the Dockerfile
docker build -t test_api .

# Run Container - run entrypoint/cmd automatically
docker run --rm --name ccb-test_api -ti \
-p 8000:8000 \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/../../../secrets \
-v ~/.gitconfig:/etc/gitconfig \
-e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
test_api
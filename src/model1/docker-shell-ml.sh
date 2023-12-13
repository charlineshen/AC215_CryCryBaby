#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/

# # Create the network if we don't have it yet
# docker network inspect ccb-preprocessing-network >/dev/null 2>&1 || docker network create ccb-preprocessing-network

# Build the image based on the Dockerfile
docker build -t ccb-model1 .

# # Run Container
# docker run --rm --name ccb-preprocessing \
# -v "$BASE_DIR":/app \
# -v "$SECRETS_DIR":/../../../secrets \
# -v ~/.gitconfig:/etc/gitconfig \
# -e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
# ccb-preprocessing cli.py

# For running locally (not vertex ai)
# Run Container with Interactive Shell
docker run --rm -it --name ccb-model1 \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ccb.json \
ccb-model1

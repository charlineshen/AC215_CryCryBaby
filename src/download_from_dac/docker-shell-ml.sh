#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/

# Build the image based on the Dockerfile
docker build -t ccb-download_from_dac .

# Production mode: Run using entrypoint and cmd in dockerfile
docker run --rm --name ccb-download_from_dac \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/../../../secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
ccb-download_from_dac cli.py

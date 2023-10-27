#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/

# Parse the runtime argument (1 for development mode, 0 for production mode)
DEV_FLAG="$1"

if [[ -z "$DEV_FLAG" ]]; then
    echo "Usage: $0 <dev_flag> (1 launches shell, and 0 launches microservice)"
    exit 1
fi

# Create the network if we don't have it yet
docker network inspect ccb-model-network >/dev/null 2>&1 || docker network create ccb-model-network

# Build the image based on the Dockerfile
docker build -t model .

# Run the container with different options based on the development flag
if [[ "$DEV_FLAG" -eq 1 ]]; then
    # Development mode: Run with an interactive bash shell
    docker run --rm --name ccb-model -ti --entrypoint /bin/bash \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/../../../secrets \
    -v ~/.gitconfig:/etc/gitconfig \
    -e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
    --network ccb-model-network model
else
    # Production mode: Run using entrypoint and cmd in dockerfile
    docker run --rm --name ccb-model \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/../../../secrets \
    -v ~/.gitconfig:/etc/gitconfig \
    -e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
    --network ccb-model-network model
fi
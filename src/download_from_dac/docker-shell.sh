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
docker network inspect ccb-download_from_dac-network >/dev/null 2>&1 || docker network create ccb-download_from_dac-network

# Build the image based on the Dockerfile
docker build -t ccb-download_from_dac .

# Run the container with different options based on the development flag
if [[ "$DEV_FLAG" -eq 1 ]]; then
    # Development mode: Run with an interactive bash shell
    docker run --rm --name ccb-download_from_dac -ti --entrypoint /bin/bash \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/../../../secrets \
    -v ~/.gitconfig:/etc/gitconfig \
    -e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
    --network ccb-download_from_dac-network ccb-download_from_dac
else
    # Production mode: Run using entrypoint and cmd in dockerfile
    docker run --rm --name ccb-download_from_dac \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/../../../secrets \
    -v ~/.gitconfig:/etc/gitconfig \
    -e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
    --network ccb-download_from_dac-network ccb-download_from_dac
fi

#!/bin/bash

# set -e

# export BASE_DIR=$(pwd)
# export SECRETS_DIR=$(pwd)/secrets/

# # Create the network if we don't have it yet
# docker network inspect ccb-download_from_dac-network >/dev/null 2>&1 || docker network create ccb-download_from_dac-network

# # Build the image based on the Dockerfile
# docker build -t download_from_dac .

# # Run Container
# docker run --rm --name ccb-download_from_dac -ti --entrypoint /bin/bash \
# -v "$BASE_DIR":/app \
# -v "$SECRETS_DIR":/secrets \
# -v ~/.gitconfig:/etc/gitconfig \
# -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ccb.json
# --network ccb-download_from_dac-network download_from_dac
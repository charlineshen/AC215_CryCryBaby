#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/secrets/

# Create the network if we don't have it yet
docker network inspect ccb-download_from_dac-network >/dev/null 2>&1 || docker network create ccb-download_from_dac-network

# Build and tag the Docker image with the commit hash
docker build -t us-east1-docker.pkg.dev/ac215-project-400018/ac215-crycrybaby-ar/download_from_dac:latest .

# Push the image to the registry
docker push us-east1-docker.pkg.dev/ac215-project-400018/ac215-crycrybaby-ar/download_from_dac:latest

#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCS_BUCKET_NAME="baby-cry-bucket"
export GCP_PROJECT="ac215-project"
export GCP_ZONE="us-west2-a"
export GCS_BUCKET_URI="gs://baby-cry-bucket"

# Create the network if we don't have it yet
docker network inspect data-versioning-network >/dev/null 2>&1 || docker network create data-versioning-network

# Build the image based on the Dockerfile
docker build -t ccb-data-versioning --platform=linux/arm64/v8 -f Dockerfile .

# Run Container
docker run --rm --name ccb-data-versioning -ti --entrypoint /bin/bash \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/../../../secrets \
-v ~/.gitconfig:/etc/gitconfig \
-e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GCS_BUCKET_URI=$GCS_BUCKET_URI \
--network data-versioning-network ccb-data-versioning


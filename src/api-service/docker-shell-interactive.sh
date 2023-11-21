#!/bin/bash

# Set image name
export IMAGE_NAME="src-frontend-react"

echo "Starting docker-shell-interactive.sh"

# Build the Docker image
docker build -t $IMAGE_NAME -f Dockerfile .

echo "Running docker container"

# Run the Docker container with volume mounts and environment variable
docker run --rm --name $IMAGE_NAME -ti -p 9000:9000 \
    -v $(pwd):/app/stuff \
    -v ./../../../secrets:/secrets \
    -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ccb.json \
    --entrypoint /bin/bash $IMAGE_NAME


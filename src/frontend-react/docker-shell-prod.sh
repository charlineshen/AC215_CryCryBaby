#!/bin/bash

set -e

export IMAGE_NAME="frontend-react"

docker build -t $IMAGE_NAME -f Dockerfile .
docker run --rm --name $IMAGE_NAME -ti -p 80:80 --entrypoint /bin/bash $IMAGE_NAME
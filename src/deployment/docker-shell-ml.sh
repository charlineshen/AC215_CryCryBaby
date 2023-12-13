#!/bin/bash

# exit immediately if a command exits with a non-zero status
#set -e

# Define some environment variables
export IMAGE_NAME="ccb-app-deployment"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="ac215-project-400018"
export GCP_ZONE="us-east1-b"
export GOOGLE_APPLICATION_CREDENTIALS=../../../secrets/deployment.json

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run the pipeline ci/cd task
# docker run --rm --name ccb-app-deployment \
#             -v /var/run/docker.sock:/var/run/docker.sock \
#             -v "$BASE_DIR/../download_from_dac":/download_from_dac \
#             -v "$BASE_DIR/../preprocessing":/preprocessing \
#             -v "$SECRETS_DIR":/secrets \
#             -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/deployment.json \
#             -e USE_GKE_GCLOUD_AUTH_PLUGIN=True \
#             -e GCP_PROJECT=ac215-project-400018 \
#             -e GCP_ZONE=us-east1-b \
#             -e GCS_BUCKET_NAME=ccb-app-ml-workflow \
#             -e GCS_SERVICE_ACCOUNT=deployment-630@ac215-project-400018.iam.gserviceaccount.com \
#             -e GCP_REGION=us-east1 \
#             ccb-app-deployment sh run-ml-pipeline.sh

docker run --rm -it \
           -v /var/run/docker.sock:/var/run/docker.sock \
           -v "$BASE_DIR/../download_from_dac":/download_from_dac \
           -v "$BASE_DIR/../preprocessing":/preprocessing \
           -v "$BASE_DIR/../model1":/model1 \
           -v "$BASE_DIR/../model2":/model2 \
           -v "$SECRETS_DIR":/secrets \
           -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/deployment.json \
           -e USE_GKE_GCLOUD_AUTH_PLUGIN=True \
           -e GCP_PROJECT=ac215-project-400018 \
           -e GCP_ZONE=us-east1-b \
           -e GCS_BUCKET_NAME=ccb-app-ml-workflow \
           -e GCS_SERVICE_ACCOUNT=deployment-630@ac215-project-400018.iam.gserviceaccount.com \
           -e GCP_REGION=us-east1 \
           ccb-app-deployment /bin/bash

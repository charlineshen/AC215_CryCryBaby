#!/bin/bash

# Set variables
PROJECT_ID="ac215-project-400018"
IMAGE_NAME="test-api"
IMAGE_TAG="latest"
REGION="us-east1"  # e.g., us-central1
REPOSITORY="ac215-crycrybaby-ar"  # Name of your Artifact Registry repository

# Authenticate with GCP (if not already authenticated)
gcloud auth login

# Set the GCP project
gcloud config set project $PROJECT_ID

# Build the Docker image
docker build -t $IMAGE_NAME .

# Tag the image for Artifact Registry
docker tag $IMAGE_NAME $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG

# Push the image to Artifact Registry
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG

echo "Image pushed to Artifact Registry successfully."
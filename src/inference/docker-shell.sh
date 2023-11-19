# # !/bin/bash
# # tensorflow-aarch64 = "*"
# # protobuf = "==4.24.4"

# # exit immediately if a command exits with a non-zero status
# set -e

# # Define some environment variables
# export IMAGE_NAME="inference"
# export BASE_DIR=$(pwd)
# export SECRETS_DIR=$(pwd)/../../../secrets/
# # # export SECRETS_DIR=$(pwd)/../../../secrets/ccb.json
# # # export PERSISTENT_DIR=$(pwd)/../persistent-folder/
# # # export GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json
# # export GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json

# # Create the network if we don't have it yet
# # docker network inspect ccb-inference-network >/dev/null 2>&1 || docker network create ccb-inference-network

# # # Build the image based on the Dockerfile
# # # docker build -t $IMAGE_NAME -f Dockerfile .
# docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .
# # docker build -t $IMAGE_NAME .

# # Run the container
# docker run --rm --name $IMAGE_NAME -ti \
# --mount type=bind,source="$BASE_DIR",target=/app $IMAGE_NAME
# -v "$BASE_DIR":/app \
# -v "$SECRETS_DIR":/../../../secrets \
# -v ~/.gitconfig:/etc/gitconfig \
# -e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \

# # -v "$SECRETS_DIR":/../../../secrets \ 
# # -v "$SECRETS_DIR" \ 
# -v "$BASE_DIR":/app \
# -v "$SECRETS_DIR":/../../../secrets \
# -v ~/.gitconfig:/etc/gitconfig \
# # -e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
# # -e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
# # -e GOOGLE_APPLICATION_CREDENTIALS="$SECRETS_DIR" \



# !/bin/bash 
# // shebang, should always be first line of script
# tells interpreter that this is the binary used to run this file

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/

# Create the network if we don't have it yet
docker network inspect ccb-inference-network >/dev/null 2>&1 || docker network create ccb-inference-network

# Build the image based on the Dockerfile
docker build -t inference .

# Run Container
docker run --rm --name ccb-inference -ti --entrypoint /bin/bash \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/../../../secrets \
-v ~/.gitconfig:/etc/gitconfig \
-e GOOGLE_APPLICATION_CREDENTIALS=/../../../secrets/ccb.json \
--network ccb-inference-network inference
#!/bin/bash

# For launching into interactive mode to update pipenv lock, etc.
# Once in terminal, run `pipenv lock` to update Pipfile.lock
# Then run `exit` to exit the container
# Then push the updated Pipfile.lock to git
export IMAGE_NAME="src-frontend-react"

echo "Starting docker-shell-interactive.sh"
docker build --platform linux/amd64 -t $IMAGE_NAME -f Dockerfile .
echo "Running docker container"

docker run --rm --name $IMAGE_NAME -ti -p 9000:9000 --entrypoint /bin/bash\
    -v $(pwd):/app/stuff $IMAGE_NAME \

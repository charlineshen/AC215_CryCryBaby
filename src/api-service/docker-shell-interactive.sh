#!/bin/bash

# For launching into interactive mode to update pipenv lock, etc.
# Once in terminal, run `pipenv lock` to update Pipfile.lock
# Then run `exit` to exit the container
# Then push the updated Pipfile.lock to git

docker run --rm --name api-service -ti \
    -v $(pwd):/app api-service:latest \

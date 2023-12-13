#!/bin/bash

echo "api-service container is running"

# Run your model download script
echo "Downloading model..."
pipenv run python ./api/download_models.py

# Check if the model download was successful
if [ $? -ne 0 ]; then
    echo "Model download failed, exiting..."
    exit 1
fi

echo "Model downloaded successfully."

# this will run the api/service.py file with the instantiated app FastAPI
uvicorn_server() {
    uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ "$@"
}

uvicorn_server_production() {
    pipenv run uvicorn api.service:app --host 0.0.0.0 --port 9000 --lifespan on
}

export -f uvicorn_server
export -f uvicorn_server_production

echo -en "\033[92m
The following commands are available:
    uvicorn_server
        Run the Uvicorn Server
\033[0m
"

if [ "${DEV}" = 1 ]; then
  pipenv shell
else
  uvicorn_server_production
fi


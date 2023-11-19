# Use the official Debian-hosted Python image
FROM python:3.9-slim-buster

# Tell pipenv where the shell is. 
# This allows us to use "pipenv shell" as a container entry point.
ENV PYENV_SHELL=/bin/bash
RUN mkdir -p /app
WORKDIR /app

# Add Pipfile, Pipfile.lock, all files
COPY . /app

# This is the preprocessing method
ENV GOOGLE_APPLICATION_CREDENTIALS=../../../secrets/ccb.json

# RUN pipenv sync

# Ensure we have an up to date baseline, install dependencies 
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git ffmpeg && \
    pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt && \
    pip install pipenv && \
    pipenv install

# Entry point
ENTRYPOINT ["/bin/bash"]

# Get into the pipenv shell
# CMD ["-c", "pipenv shell"]
CMD ["python", "inference_1031.py"]

## why isn't pipenv working? 
## why aren't packages being installed in the virtual environment?
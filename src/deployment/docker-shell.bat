SET IMAGE_NAME="ccb-deployment"
SET GCP_PROJECT="ac215-project-400018"
SET GCP_ZONE="us-west2-a"
SET GOOGLE_APPLICATION_CREDENTIALS=/secrets/deployment.json
docker build -t %IMAGE_NAME% -f Dockerfile .
cd ..
docker run --rm --name %IMAGE_NAME% -ti ^
           -v /var/run/docker.sock:/var/run/docker.sock ^
           --mount type=bind,source="%cd%\deployment",target=/app ^
           --mount type=bind,source="%cd%\secrets",target=/secrets ^
           --mount type=bind,source="C:\Users\<UserName>\.ssh",target=/home/app/.ssh ^
           --mount type=bind,source="%cd%\api-service",target=/api-service ^
           --mount type=bind,source="%cd%\frontend-react",target=/frontend-react ^
           -e GOOGLE_APPLICATION_CREDENTIALS="%GOOGLE_APPLICATION_CREDENTIALS%" ^
           -e GCP_PROJECT="%GCP_PROJECT%" ^
           -e GCP_ZONE="%GCP_ZONE%" %IMAGE_NAME%

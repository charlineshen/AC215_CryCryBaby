AC215 - Cry Cry Baby🍼
==============================
### Presentation  Video
* \<Link Here>

### Blog Post Link
*  \<Link Here>
---

?? kubeflow folder.
?? Run ML Tasks in Vertex AI

Project Organization
------------
      ├── LICENSE
      ├── README.md
      └── notebooks
            ├── crycrybaby_poc_cleaned.ipynb
            ├── crycrybaby_poc_wandb.ipynb
            ├── model2.ipynb
            ├── model1.ipynb
      └── src
            ├── download_from_dac
            │   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── docker-shell.sh
            │   └── download_from_dac.py
            ├── preprocessing
            │   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── docker-shell.sh
            │   └── preprocessing.py
            ├── model1
            │   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── docker-shell.sh
            │   └── model1.py
            ├── model2
            |   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── docker-shell.sh
            │   └── model2.py
            ├── api-service
            |   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── docker-shell.sh
            │   ├── service.py
            │   ├── inference.py
            │   └── download_models.py
            ├── frontend-react
            |   ├── conf
            |   ├── public
            |   ├── src
            |   |   ├── app
            |   |   ├── services
            |   |   ├── index.css
            |   |   ├── index.js
            |   ├── .env.development
            |   ├── .env.production
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── package-lock.json
            │   ├── package.json
            │   ├── yarn.lock
            │   ├── docker-shell.sh
            │   ├── Dockerfile
            │   └── Dockerfile.dev
  
# AC215 - Final Project

**Team Members**
Jessica Gochioco, Jingwen Zhang, Adam Stone, Charline Shen

**Group Name**
Cry Cry Baby

**Project - Problem Definition**
Parenting is a rewarding yet challenging journey that millions of individuals embark on each year. One of the most difficult aspects of caring for a baby is understanding and addressing their needs, especially when they have not yet learned how to talk. Our project centers on the application of the Dunstan Baby Language (DBL) , a concept suggesting that infants possess distinct vocal cues for various needs, and the development of a mobile app that leverages this knowledge. This app aims to empower parents by enabling them to decode their baby's cries and respond effectively, thereby reducing the stress associated with early parenthood. Furthermore, our project envisions a feature to have caretakers self-identify cries in order to add to our dataset, as well as the integration of a chatbot that can offer real-time support and guidance to parents.


## Data Description 

## Proposed Solution

After completions of building a robust ML Pipeline in our previous milestone we have built a backend api service and frontend app. This will be our user-facing application that ties together the various components built in previous milestones.


**Cry Cry Baby App**

A user-friendly React app was developed to identify various baby cries using machine learning models from the backend. With the app, users can record an audio file of a baby cry and upload it. The app then sends the audio to the backend API to obtain prediction results on whether the uploaded audio is indeed a baby cry and provides information on why the baby may be crying.

Here are some screenshots of our app:
<img src="images/frontend-1.png"  width="800">

<img src="images/frontend-2.png"  width="800">

**Kubernetes Deployment**

We deployed our frontend and backend to a kubernetes cluster to take care of load balancing and failover. We used ansible scripts to manage creating and updating the k8s cluster. Ansible helps us manage infrastructure as code and this is very useful to keep track of our app infrastructure as code in GitHub. It helps use setup deployments in a very automated way.

Here is our deployed app on a K8s cluster in GCP:
<img src="images/k8s.png"  width="800">


### Code Structure
The following are the folders from the previous milestones:
```
- download_from_dac: data colloector
- preprocessing: data processor
- model1: baby cry detection model
- model2: needs classification model
- api-service: backend coordinator
- frontend-react: app frontend
- deployment: auto-deployment via Ansible & Kubernetes
```

**API Service Container**
This container has all the python files to run and expose thr backend apis.

To run the container locally:
- Open a terminal and go to the location where `AC215_CryCryBaby/src/api-service`
- Run `sh docker-shell.sh`
- Once inside the docker container run `uvicorn_server`
- To view and test APIs go to `http://localhost:9000/docs`

**Frontend Container**
This container contains all the files to develop and build a react app. There are dockerfiles for both development and production

To run the container locally:
- Open a terminal and go to the location where `AC215_CryCryBaby/src/frontend-react`
- Run `sh docker-shell.sh`
- Go to `http://localhost:3000` to access the app locally


**Deployment Container**
This container helps manage building and deploying all our app containers. The deployment is to GCP and all docker images go to GCR. 

To run the container locally:
- Open a terminal and go to the location where `AC215_CryCryBaby/src/deployment`
- Run `sh docker-shell.sh`
- Build and Push Docker Containers to GCR (Google Container Registry)
```
ansible-playbook deploy-docker-images.yml -i inventory.yml
```

- Create & Deploy Cluster
```
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present
```

- View the App
* Copy the `nginx_ingress_ip` from the terminal from the create cluster command
* Go to `http://34.75.108.68.sslip.io/`

<!-- - ?? Run ML Tasks in Vertex AI ??
* Run `python cli.py --data_collector`, run just the data collector on Vertex AI
* Run `python cli.py --data_processor`, run just the data processor on Vertex AI
* Run `python cli.py --pipeline`, run the entire ML pipeline in Vertex AI -->


<!-- ### Deploy using GitHub Actions

Finally we added CI/CD using GitHub Actions, such that we can trigger deployment or any other pipeline using GitHub Events. Our yaml files can be found under `.github/workflows`

`cicdworkflow.yml` - Brief description here

We implemented a CI/CD workflow to use the deployment container to 
* Invoke docker image building and pushing to GCR on code changes
* Deploy the changed containers to update the k8s cluster
* Run Vertex AI jobs if needed -->


## NOTE

**DO NOT KEEP YOUR GCP INSTANCES RUNNING**

Once you are done with taking screenshots for the milestone bring them down. 


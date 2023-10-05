AC215-Milestone3
==============================

AC215 - Milestone3

Project Organization
------------
      ├── LICENSE
      ├── README.md
      ├── requirements.txt
      └── src
            ├── preprocessing
            │   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── docker-shell.sh
            │   └── preprocessing.py
            ├── dataversion
            │   ├── Dockerfile
            │   ├── Pipfile
            │   ├── Pipfile.lock
            │   ├── docker-shell.sh
            │   └── preprocessing.py
            └── model
                  ├── Dockerfile
              │   ├── Pipfile
              │   ├── Pipfile.lock
              │   ├── docker-shell.sh
              │   └── model.py
  

--------
# AC215 - Milestone3 - Cry Cry Baby

**Team Members**
Jessica Gochioco, Jingwen Zhang, Adam Stone, Charline Shen


**Group Name**
Cry Cry Baby

**Project**
Parenting is a rewarding yet challenging journey that millions of individuals embark on each year. One of the most difficult aspects of caring for a baby is understanding and addressing their needs, especially when they have not yet learned how to talk. Our project centers on the application of the Dunstan Baby Language (DBL) , a concept suggesting that infants possess distinct vocal cues for various needs, and the development of a mobile app that leverages this knowledge. This app aims to empower parents by enabling them to decode their baby's cries and respond effectively, thereby reducing the stress associated with early parenthood. Furthermore, our project envisions a feature to have caretakers self-identify cries in order to add to our dataset, as well as the integration of a chatbot that can offer real-time support and guidance to parents.


### Milestone3 ###
Our main datasource will come from the Donate-a-Cry Corpus  (https://github.com/gveres/donateacry-corpus/tree/master, cleaned and updated version). We parked our dataset in a private Google Cloud Bucket. 


**Preprocess container**
- This container reads all the audio files (in .wav format), translate them into spectrogram (in .txt format), and stores it back to GCP
- Source and destincation GCS location are preset in cli.py. Input to this container is secrets files - via docker
- Output from this container stored at GCS location

(1) `src/preprocessing/preprocessing.py`  - Here we first download audio files from GCP,  convert our audio files into numerical representation called spectrogram, normalize each matrices, and save the X & y data for our model on GCS. 

(2) `src/preprocessing/Dockerfile` - This dockerfile starts with  `python:3.8-slim-buster`. This <statement> attaches volume to the docker container and also uses secrets to connect to GCS.

(3) `src/preprocessing/Pipfile` - This file will be used by the Pipenv virtual environment to manage project dependencies.

(4) `src/preprocessing/Pipfile.lock` - This file replaces the requirements. txt file used in most Python projects and adds security benefits of tracking the packages hashes that were last locked

(5) `src/preprocessing/docker-shell.sh` - This shell file grabs credentials from GCP and automates the execution of Dockerfile.

**Mock Submission**


***To open the container:***

0. Send an email to charlineshen@g.harvard.edu with your email address associated with your GCP account. We would add you as an editor to our GCP project.
1. [Login GCP, select ac215-project-400018, start the VM instance] 
2. Open a GCP terminal, change directory into /home/charlineshen/AC215_CryCryBaby/src/preprocessing folder
3. Run `docker-shell.sh` using command: `sudo sh docker-shell.sh`
4. Inside the container, run preprocessing using command: `python cli.py`
5. `cli.py` would download audio files from GCP bucket, transform audio files into spectrograms(matrices in .txt files), and then upload the processed files to GCP bucket. You could observe the updates in Cloud Storage - Buckets in your GCP project.
6. Stop VM instance!

**Container 2**
TO BE UPDATED

**Notebooks** 
 To BE UPDATED (This folder contains code that is not part of container - for e.g: EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations.)


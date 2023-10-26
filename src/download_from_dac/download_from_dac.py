from google.cloud import storage
import os
import subprocess

# This file downloads files from the donate-a-cry github and uploads it to our GCP bucket.

gcp_project = "ac215-project"
bucket_name = "baby-cry-bucket"
output_folder = "donateacry-corpus-raw-data"
labels = ['belly_pain', 'burping', 'discomfort', 'hungry', 'tired']

# Initialize empty lists to store WAV file paths and folder names
wav_files = []
folder_names = []

# Make sure that the target folders already exist, otherwise, create them
def makedirs():
    os.makedirs(output_folder, exist_ok=True)

    for label in labels:
        os.makedirs(output_folder+'/'+ label, exist_ok=True)

# Download data from donate-a-cry dataset
def download_donate_corpus():
    # Define the GitHub repository URL
    github_repo_url = "https://github.com/gveres/donateacry-corpus.git"

    # Clone the repository
    subprocess.run(["git", "clone", github_repo_url])

    # Define the path to the cloned repository
    repo_path = "donateacry-corpus"

    # Walk through the directory structure to find WAV files and their folders
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".wav"):
                # Get the full path of the WAV file
                wav_path = os.path.join(root, file)

                # Extract the folder name from the path
                folder_name = os.path.basename(root)

                # Append the WAV file path and folder name to the respective lists
                wav_files.append(wav_path)
                folder_names.append(folder_name)


# Download esc50 data
def download_esc50():
    github_repo_url = "https://github.com/karolpiczak/ESC-50.git"
    # Clone the repository
    subprocess.run(["git", "clone", github_repo_url])

# Download crema_d data -- NOT WORKING YET!
def download_crema_d():
    github_repo_url = "https://github.com/CheyneyComputerScience/CREMA-D.git"
    # Clone the repository
    # subprocess.run(['git', 'config', '--system', 'core.longpaths', 'true'])
    subprocess.run(["git", "clone", github_repo_url])

def get_dac():
    print("Getting donate-a-cry data...")
    download_donate_corpus()
    print("Getting ESC50 data...")
    download_esc50()
    # print("Getting CREMA-D data...")
    # download_crema_d()
    

def upload_donate_corpus():
    # Initialize the GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for i in range(len(wav_files)):
        spct_file = wav_files[i]
        label = folder_names[i]

        # Specify the remote destination path including the label folder
        destination_blob_name = f"{output_folder}/{label}/{os.path.basename(spct_file)}"

        # Create a blob in the bucket
        blob = bucket.blob(destination_blob_name)

        # Upload the local file to the blob
        blob.upload_from_filename(spct_file)

def upload_esc50():
    # Initialize the GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Define the path to the cloned repository
    repo_path = "ESC-50"

    output_folder = 'ESC-50-raw-data'

    # Walk through the directory structure to find WAV files and their folders
    for dir in os.listdir(repo_path):
        dir_path = os.path.join(repo_path, dir)
        if os.path.isdir(dir_path) and dir == 'audio' or dir == 'meta':
            for file in os.listdir(dir_path):
                if file.endswith(".wav"):
                    file_path = os.path.join(dir_path, file)
                    # Specify the remote destination path including the label folder
                    destination_blob_name = f"{output_folder}/{dir}/{file}"

                    # Create a blob in the bucket
                    blob = bucket.blob(destination_blob_name)

                    # Upload the local file to the blob
                    blob.upload_from_filename(file_path)


def upload_crema_d():
    # Initialize the GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Define the path to the cloned repository
    repo_path = "CREMA-D"

    output_folder = 'CREMA-D-raw-data'

    # Walk through the directory structure to find WAV files and their folders
    for dir in os.listdir(repo_path):
        dir_path = os.path.join(repo_path, dir)
        if os.path.isdir(dir_path) and dir == 'AudioWAV':
            for file in os.listdir(dir_path):
                if file.endswith(".wav"):
                    file_path = os.path.join(dir_path, file)
                    # Specify the remote destination path including the label folder
                    destination_blob_name = f"{output_folder}/{dir}/{file}"

                    # Create a blob in the bucket
                    blob = bucket.blob(destination_blob_name)

                    # Upload the local file to the blob
                    blob.upload_from_filename(file_path)


# Revised upload function
def upload():
    print("Uploading donate-a-cry...")
    upload_donate_corpus()
    print("Uploading ESC 50...")
    upload_esc50()
    # print("Uploading CREMA-D...")
    # upload_crema_d()
    print("Upload finished!")


def main(args=None):
    makedirs()
    get_dac()
    upload()


if __name__ == "__main__":
    main()
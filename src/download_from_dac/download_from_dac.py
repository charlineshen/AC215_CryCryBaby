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

def get_dac():
    print("Getting donate-a-cry data...")

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

# Original upload function          
# def upload():
#     print("upload")

#     # Upload to bucket
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)

#     # Get the list of files
#     spct_files = os.listdir(output_folder)

#     for spct_file in spct_files:
#         # specify output filepath
#         file_path = os.path.join(output_folder, spct_file)

#         destination_blob_name = file_path
#         blob = bucket.blob(destination_blob_name)
#         blob.upload_from_filename(file_path)

# Revised upload function
def upload():
    print("Uploading...")

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
    
    print("Upload finished!")



def main(args=None):
    makedirs()
    get_dac()
    upload()


if __name__ == "__main__":
    main()
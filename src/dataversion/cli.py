"""
Module that contains the command line app.
"""
import os
from google.cloud import storage
import numpy as np

gcp_project = "ac215-project"
bucket_name = "baby-cry-bucket"
output_folder = "output_data_augmentation"
input_folder = "input_spectrogram"


def makedirs():
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(input_folder, exist_ok=True)

def download():
    print("download")

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)
    folder_name = "output_spectrogram/"

    # Iterate through the labels
    blobs = bucket.list_blobs(prefix = folder_name)

    for blob in blobs:
        if blob.name.endswith(".npy"):
            print(blob.name)
            blob.download_to_filename("/app/" + input_folder +"/" + blob.name[len(folder_name):])
    
    return

def load_data():
    X = np.load("/app/" + input_folder + '/' + 'X.npy')
    y = np.load("/app/" + input_folder + '/' + 'y.npy')

    return X, y


def data_augmentation(X, y):
    print("Start Data Augmentation")
    np.random.seed(seed=217)
    X_fake = np.random.rand(X.shape[0], X.shape[1], X.shape[2])/100 + X
    X_augmented = np.concatenate((X, X_fake), axis=0)
    y_augmented = np.concatenate((y, y), axis=0)

    print("X_augmented Shape:", X_augmented.shape)
    print("y_augmented Shape:", y_augmented.shape)

    output_path = "/app/"+output_folder
    np.save(output_path + '/' + 'X.npy',  X_augmented)
    np.save(output_path + '/' + 'y.npy',  y_augmented)

    return


def main(args=None):
    makedirs()
    download()
    X, y = load_data()
    data_augmentation(X, y)

if __name__ == "__main__":
    main()
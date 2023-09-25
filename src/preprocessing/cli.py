"""
Module that contains the command line app.
"""
import os
import argparse
import shutil
import librosa
import numpy as np
import librosa.display
from google.cloud import storage


## upload secrets to GCP & pull from there in code

gcp_project = "ac215-project"
bucket_name = "baby-cry-bucket"
output_spectrogram = "output_spectrogram"
input_wav = "input_wav"

def makedirs():
    os.makedirs(output_spectrogram, exist_ok=True)
    os.makedirs(input_wav, exist_ok=True)


def download():
    print("download")

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix="donateacry-corpus-raw-data/")

    for blob in blobs:
        if blob.name.endswith(".wav"):
            # JZ note: to update
            blob.download_to_filename("input_wav/" + blob.name[len("donateacry-corpus-raw-data/"):])



def wav_to_spectrogram(input_path = "/app/input_wav/", output_path = "/app/output_spectrogram", output_shape=(128, 64)):
    
    for file_name in os.listdir(input_path):
        # Load the WAV file
        y, sr = librosa.load(input_path+file_name, sr=None)

        # Generate the spectrogram
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

        # Resize the spectrogram to the desired shape (e.g., 128x64)
        spectrogram = librosa.util.fix_length(spectrogram, size=output_shape[1], mode='constant', constant_values=0)

        # Normalize the spectrogram to values between 0 and 1
        spectrogram = librosa.util.normalize(spectrogram)

        # JZ note: to update
        np.savetxt(output_path + '/' + file_name[:-4] +'.txt', spectrogram, fmt='%f')


    return spectrogram, sr


def upload():
    print("upload")

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of files
    spct_files = os.listdir(output_spectrogram)

    for spct_file in spct_files:
        # specify output filepath
        file_path = os.path.join(output_spectrogram, spct_file)

        destination_blob_name = file_path
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)


def main(args=None):
    makedirs()
    download()
    wav_to_spectrogram()
    upload()


if __name__ == "__main__":
    main()


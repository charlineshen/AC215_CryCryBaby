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
output_folder = "output_spectrogram"
input_folder = "input_wav"
labels = ['belly_pain', 'burping', 'discomfort', 'hungry', 'tired']


def makedirs():
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(input_folder, exist_ok=True)

    for label in labels:
        os.makedirs(input_folder+'/'+ label, exist_ok=True)
    


def download():
    print("download")

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)

    folder_name = "donateacry-corpus-raw-data/"

    # Iterate through the labels
    for label_idx, label in enumerate(labels):
        blobs = bucket.list_blobs(prefix = folder_name + label + "/")
        print("loading: " + folder_name +label+"/")
        for blob in blobs:
            if blob.name.endswith(".wav"):
                # JZ note: to update
                blob.download_to_filename("/app/" + input_folder +"/" + blob.name[len(folder_name):])
        print("loaded: " + folder_name +label+"/")


def wav_to_spectrogram(input_path, output_shape=(128, 64)):
    

    # Load the WAV file
    y, sr = librosa.load(input_path, sr=8000, dtype=np.float32)

    # Generate the spectrogram
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

    # Resize the spectrogram to the desired shape (e.g., 128x64)
    spectrogram = librosa.util.fix_length(spectrogram, size=output_shape[1], mode='constant', constant_values=0)

    # Normalize the spectrogram to values between 0 and 1
    spectrogram = librosa.util.normalize(spectrogram)

    return spectrogram, sr




def preprocessing(output_path = "/app/"+output_folder, ):
    # Define the folder containing the subfolders with WAV files
    data_folder = 'donateacry_corpus_cleaned_and_updated_data'

    # Define the labels (subfolder names)
    labels = ['belly_pain', 'burping', 'discomfort', 'hungry', 'tired']

    # Initialize empty lists to store spectrograms and labels
    X = []
    y = []

    # Iterate through the labels
    for label_idx, label in enumerate(labels):
        label_folder = os.path.join("/app", input_folder, label)

        # Iterate through WAV files in the label folder
        for wav_file in os.listdir(label_folder):
            if wav_file.endswith('.wav'):
                wav_file_path = os.path.join(label_folder, wav_file)

                # Convert WAV to spectrogram using the wav_to_spectrogram function
                spectrogram, sr = wav_to_spectrogram(wav_file_path)

                # Append the spectrogram to X_train
                X.append(spectrogram)

                # Append the label index (numeric representation of the label) to y_train
                y.append(label_idx)

    # Convert lists to NumPy arrays for further processing
    X = np.array(X)
    y = np.array(y)

    # Check the shapes
    print(f'X shape: {X.shape}')
    print(f'y shape: {y.shape}')

    np.save(output_path + '/' + 'X.npy',  X)
    np.save(output_path + '/' + 'y.npy',  y)
    return 


def upload():
    print("upload")

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of files
    spct_files = os.listdir(output_folder)

    for spct_file in spct_files:
        # specify output filepath
        file_path = os.path.join(output_folder, spct_file)

        destination_blob_name = file_path
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)


def main(args=None):
    makedirs()
    download()
    preprocessing()
    upload()


if __name__ == "__main__":
    main()


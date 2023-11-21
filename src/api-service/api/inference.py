import librosa
import numpy as np
import matplotlib.pyplot as plt
from google.cloud import storage
import os
import tensorflow as tf


# Define the GCP project and bucket names
gcp_project = "ac215-project"
bucket_name = "baby-cry-bucket" 
bucket_prefix = "output_model/"
bucket_name_test_audio = "baby-cry-inference-test"
test_audio = "theo_tired_trimmed"
models = ["model1_v1.h5", "model2_v1.h5"]

# Take test audio from GCS bucket
def download_test_audio():
    print("downloading test audio...")

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name_test_audio)
    
    blob = bucket.blob(test_audio + ".wav")
    blob.download_to_filename(test_audio + ".wav")

def wav_to_spectrogram(file_path, output_shape=(128, 64)):
    print("converting wav to spectrogram...")
    # Load the WAV file
    y, sr = librosa.load(file_path, sr=8000, dtype=np.float32)

    # Generate the spectrogram
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    
    # Resize the spectrogram so that it can be fed into the model
    spectrogram = librosa.util.fix_length(spectrogram, size=output_shape[1], mode='constant', constant_values=0)
    
    # Normalize the spectrogram to values between 0 and 1, this really helps improve model accuracy
    spectrogram = librosa.util.normalize(spectrogram)

    return spectrogram, sr, y

# Get our saved model from GCP
def download_models():
    print("downloading models...")

    # Clear
    # shutil.rmtree(text_paragraphs, ignore_errors=True, onerror=None)
    # makedirs()

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)

    # Download model 1

    # Combine bucket prefix and model name
    model1_path = os.path.join(bucket_prefix, models[0])

    blob = bucket.blob(model1_path)
    blob.download_to_filename(models[0])

    # Download model 2
    model2_path = os.path.join(bucket_prefix, models[1])
    blob = bucket.blob(model2_path)
    blob.download_to_filename(models[1])

    model1 = tf.keras.models.load_model(models[0])
    model2 = tf.keras.models.load_model(models[1])

    return model1, model2

# def get_wandb_model():
#     run = wandb.init()
#     artifact = run.use_artifact('ac215-ccb/model-registry/misunderstood-deluge-simple:v0', type='model')
#     artifact_dir = artifact.download()
#     model = tf.keras.models.load_model(artifact_dir)
#     return model

# Define a dictionary to map the index to the corresponding label
label_map = {
    0: 'belly_pain',
    1: 'burp',
    2: 'discomfort',
    3: 'hungry',
    4: 'tired'
}

def get_prediction(model1, model2, spectrogram):
    ##### Do model 1 predictions #####
    # Need the [0] because of the way it's formatted
    m1_predictions = model1.predict(spectrogram)[0]

    ##### Do model 2 predictions #####
    # Perform predictions using the loaded model
    m2_predictions = model2.predict(spectrogram)[0]

    # Use argmax to find the most likely prediction
    m2_predicted_label_index = m2_predictions.argmax()

    # Map the index to the corresponding label
    m2_predicted_label = label_map[m2_predicted_label_index]

    print({"cry": m1_predictions[1],
            "label": m2_predicted_label,
            "prob": m2_predictions[m2_predicted_label_index]
    })

    return {"cry": m1_predictions[1],
            "label": m2_predicted_label,
            "prob": m2_predictions[m2_predicted_label_index]
    }

def predict():

    # TODO remove this test code
    return {"cry": .50,
            "label": "belly_pain",
            "prob": .50}
    
    download_test_audio()
    # print("test audio downloaded...")
    spectrogram, sr, y = wav_to_spectrogram(test_audio + ".wav")
    # print("spectrogram generated...")
    model1, model2 = download_models()
    # print("models downloaded...")
    spectrogram = np.reshape(spectrogram, (1, 128, 64))
    # print("spectrogram reshaped...")
    get_prediction(model1, model2, spectrogram)
    # print("prediction complete...")
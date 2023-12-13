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
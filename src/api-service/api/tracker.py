import os
import traceback
import asyncio
from glob import glob
import json
import pandas as pd

import tensorflow as tf
from google.cloud import storage


bucket_name = os.environ["GCS_BUCKET_NAME"]
local_experiments_path = "/persistent/experiments"

# Setup experiments folder
if not os.path.exists(local_experiments_path):
    os.mkdir(local_experiments_path)


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def download_experiment_metrics():
    # Get all model metrics
    models_metrics_list = tf.io.gfile.glob(
        "gs://" + bucket_name + "/*/*_model_metrics.json"
    )

    timestamp = 0

    for metrics_file in models_metrics_list:
        path_splits = metrics_file.split("/")
        experiment = path_splits[-2]
        local_metrics_file = path_splits[-1]

        local_metrics_file = os.path.join(
            local_experiments_path, experiment, local_metrics_file
        )

        if not os.path.exists(local_metrics_file):
            print("Copying:", metrics_file, local_metrics_file)

            # Ensure user directory exists
            os.makedirs(local_experiments_path, exist_ok=True)
            os.makedirs(
                os.path.join(local_experiments_path, experiment),
                exist_ok=True,
            )

            metrics_file = metrics_file.replace("gs://" + bucket_name + "/", "")
            # Download the metric json file
            download_blob(bucket_name, metrics_file, local_metrics_file)

            file_timestamp = os.path.getmtime(local_metrics_file)
            if file_timestamp > timestamp:
                timestamp = file_timestamp

    return timestamp


def agg_experiments():
    print("Aggregate all experiments across users")

    # Get Experiments accross users
    models_metrics_list = glob(local_experiments_path + "/*/*_model_metrics.json")

    all_models_metrics = []
    for mm_file in models_metrics_list:
        path_splits = mm_file.split("/")

        with open(mm_file) as json_file:
            model_metrics = json.load(json_file)
            model_metrics["experiment"] = path_splits[-2]
            model_metrics["model_name"] = path_splits[-1].replace(
                "_model_metrics.json", ""
            )
            all_models_metrics.append(model_metrics)

    # Convert to dataframe and save as csv
    experiments = pd.DataFrame(all_models_metrics)
    experiments = experiments.sort_values(by=["accuracy"], ascending=False)
    experiments.to_csv(local_experiments_path + "/experiments.csv", index=False)


def download_best_model():
    print("Download best model")
    try:
        experiments = pd.read_csv(local_experiments_path + "/experiments.csv")
        print("Shape:", experiments.shape)
        print(experiments.head())

        # Find the overall best model across users
        best_model = experiments.iloc[0].to_dict()
        # Create a json file best_model.json
        with open(
            os.path.join(local_experiments_path, "best_model.json"), "w"
        ) as json_file:
            json_file.write(json.dumps(best_model))

        # Download model
        download_file = os.path.join(
            best_model["experiment"], best_model["model_name"] + ".keras"
        )
        download_blob(
            bucket_name,
            download_file,
            os.path.join(local_experiments_path, download_file),
        )

        download_file = os.path.join(
            best_model["experiment"],
            best_model["model_name"] + "_train_history.json",
        )
        download_blob(
            bucket_name,
            download_file,
            os.path.join(local_experiments_path, download_file),
        )

        # Data details
        download_file = os.path.join(best_model["experiment"], "data_details.json")
        download_blob(
            bucket_name,
            download_file,
            os.path.join(local_experiments_path, download_file),
        )

    except:
        print("Error in download_best_model")
        traceback.print_exc()


class TrackerService:
    def __init__(self):
        self.timestamp = 0

    async def track(self):
        while True:
            await asyncio.sleep(60)
            print("Tracking experiments...")

            # Download new model metrics
            timestamp = download_experiment_metrics()

            if timestamp > self.timestamp:
                # Aggregate all experiments across users
                agg_experiments()

                # Download best model
                download_best_model()

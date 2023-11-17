import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.keras.models import Model
import tensorflow_hub as hub
from google.cloud import aiplatform
import base64


AUTOTUNE = tf.data.experimental.AUTOTUNE
local_experiments_path = "/persistent/experiments"
best_model = None
best_model_id = None
prediction_model = None
data_details = None
image_width = 224
image_height = 224
num_channels = 3


def load_prediction_model():
    print("Loading Model...")
    global prediction_model, data_details

    best_model_path = os.path.join(
        local_experiments_path,
        best_model["experiment"],
        best_model["model_name"] + ".keras",
    )

    print("best_model_path:", best_model_path)
    prediction_model = tf.keras.models.load_model(
        best_model_path, custom_objects={"KerasLayer": hub.KerasLayer}
    )
    print(prediction_model.summary())

    data_details_path = os.path.join(
        local_experiments_path, best_model["experiment"], "data_details.json"
    )

    # Load data details
    with open(data_details_path, "r") as json_file:
        data_details = json.load(json_file)


def check_model_change():
    global best_model, best_model_id
    best_model_json = os.path.join(local_experiments_path, "best_model.json")
    if os.path.exists(best_model_json):
        with open(best_model_json) as json_file:
            best_model = json.load(json_file)

        if best_model_id != best_model["experiment"]:
            load_prediction_model()
            best_model_id = best_model["experiment"]


def load_preprocess_image_from_path(image_path):
    print("Image", image_path)

    image_width = 224
    image_height = 224
    num_channels = 3

    # Prepare the data
    def load_image(path):
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=num_channels)
        image = tf.image.resize(image, [image_height, image_width])
        return image

    # Normalize pixels
    def normalize(image):
        image = image / 255
        return image

    test_data = tf.data.Dataset.from_tensor_slices(([image_path]))
    test_data = test_data.map(load_image, num_parallel_calls=AUTOTUNE)
    test_data = test_data.map(normalize, num_parallel_calls=AUTOTUNE)
    test_data = test_data.repeat(1).batch(1)

    return test_data


def make_prediction(image_path):
    check_model_change()

    # Load & preprocess
    test_data = load_preprocess_image_from_path(image_path)

    # Make prediction
    prediction = prediction_model.predict(test_data)
    idx = prediction.argmax(axis=1)[0]
    prediction_label = data_details["index2label"][str(idx)]

    if prediction_model.layers[-1].activation.__name__ != "softmax":
        prediction = tf.nn.softmax(prediction).numpy()
        print(prediction)

    poisonous = False
    if prediction_label == "amanita":
        poisonous = True

    return {
        "input_image_shape": str(test_data.element_spec.shape),
        "prediction_shape": prediction.shape,
        "prediction_label": prediction_label,
        "prediction": prediction.tolist(),
        "accuracy": round(np.max(prediction) * 100, 2),
        "poisonous": poisonous,
    }


def make_prediction_vertexai(image_path):
    print("Predict using Vertex AI endpoint")

    # Get the endpoint
    # Endpoint format: endpoint_name="projects/{PROJECT_NUMBER}/locations/us-central1/endpoints/{ENDPOINT_ID}"
    endpoint = aiplatform.Endpoint(
        "projects/129349313346/locations/us-central1/endpoints/8600804363952193536"
    )

    with open(image_path, "rb") as f:
        data = f.read()
    b64str = base64.b64encode(data).decode("utf-8")
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = [{"bytes_inputs": {"b64": b64str}}]

    result = endpoint.predict(instances=instances)

    print("Result:", result)
    prediction = result.predictions[0]
    print(prediction, prediction.index(max(prediction)))

    index2label = {0: "oyster", 1: "crimini", 2: "amanita"}

    prediction_label = index2label[prediction.index(max(prediction))]

    poisonous = False
    if prediction_label == "amanita":
        poisonous = True

    return {
        "prediction_label": prediction_label,
        "prediction": prediction,
        "accuracy": round(np.max(prediction) * 100, 2),
        "poisonous": poisonous,
    }

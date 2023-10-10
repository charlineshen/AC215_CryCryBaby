"""
Module that contains the command line app.
"""
import os
import numpy as np
from google.cloud import storage
from tensorflow.keras import layers, models
import tensorflow as tf

# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# print(sklearn.__version__)

## upload secrets to GCP & pull from there in code

gcp_project = "ac215-project"
bucket_name = "baby-cry-bucket"
output_folder = "output_model"
input_folder = "input_spectrogram"
labels = ["belly_pain", "burping", "discomfort", "hungry", "tired"]


def makedirs():
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(input_folder, exist_ok=True)


def download():
    print("download")

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)
    folder_name = "output_spectrogram/"

    # Iterate through the labels
    blobs = bucket.list_blobs(prefix=folder_name)

    for blob in blobs:
        if blob.name.endswith(".npy"):
            print(blob.name)
            blob.download_to_filename(
                "/app/" + input_folder + "/" + blob.name[len(folder_name) :]
            )

    return


def load_data():
    X = np.load("/app/" + input_folder + "/" + "X.npy")
    y = np.load("/app/" + input_folder + "/" + "y.npy")

    return X, y


def model(X, y):
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=215)
    def shuffle_split_data(X, y):
        np.random.seed(103)
        arr_rand = np.random.rand(X.shape[0])
        split = arr_rand < np.percentile(arr_rand, 80)

        X_train = X[split]
        y_train = y[split]
        X_test = X[~split]
        y_test = y[~split]

        return X_train, X_test, y_train, y_test

    X_train, X_test, y_train, y_test = shuffle_split_data(X, y)

    # Create the model
    num_classes = len(np.unique(y_train))

    model = models.Sequential(
        [
            layers.Input(
                shape=(128, 64)
            ),  # Adjust the input shape based on your spectrogram size
            layers.Reshape(target_shape=(128, 64, 1)),  # Add a channel dimension
            layers.Conv2D(32, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )

    # Compile the model
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    # Convert labels to one-hot encoding (assuming you have more than one class)
    y_train_encoded = tf.keras.utils.to_categorical(y_train, num_classes)
    y_test_encoded = tf.keras.utils.to_categorical(y_test, num_classes)

    # Use TF data
    train_data = tf.data.Dataset.from_tensor_slices((X_train, y_train_encoded))
    validation_data = tf.data.Dataset.from_tensor_slices((X_test, y_test_encoded))

    # Train the model
    train_batch_size = 32
    val_batch_size = 16
    epochs = 1  # todo change to 10

    history = model.fit(
        train_data.batch(train_batch_size),
        epochs=epochs,
        validation_data=validation_data.batch(val_batch_size),
    )

    # Evaluate the model on the test set
    # y_pred = model.predict(X_test)
    # y_pred_classes = np.argmax(y_pred, axis=1)
    # y_test_classes = np.argmax(y_test_encoded, axis=1)

    # accuracy = accuracy_score(y_test_classes, y_pred_classes)
    # print(f'Test accuracy: {accuracy:.2f}')

    model.save("/app/" + output_folder + "/" + "model_v1.h5")

    return


def upload():
    print("upload")

    # Upload to bucket
    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)

    # Get the list of files
    spct_files = os.listdir(output_folder)

    for spct_file in spct_files:
        # specify output filepath
        file_path = os.path.join(output_folder, spct_file)

        destination_blob_name = file_path
        blob = bucket.blob(destination_blob_name)
        print("start uploading")
        try:
            blob.upload_from_filename(file_path)
            print("uploaded")
        except Exception as e:
            print(f"Exception: {e}")


def main(args=None):
    makedirs()
    download()
    X, y = load_data()
    model(X, y)
    upload()


if __name__ == "__main__":
    main()

"""
Module that contains the command line app.
# """
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import numpy as np
from google.cloud import storage
from tensorflow.keras import layers, models
import tensorflow as tf


# print(sklearn.__version__)

## upload secrets to GCP & pull from there in code

gcp_project = "ac215-project"
bucket_name = "baby-cry-bucket"
output_folder = "output_model"
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
    blobs = bucket.list_blobs(prefix=folder_name)

    for blob in blobs:
        if blob.name.endswith("_model1.npy"):
            print(blob.name)
            blob.download_to_filename(
                "/app/" + input_folder + "/" + blob.name[len(folder_name) :]
            )

    return


def load_data():
    X = np.load("/app/" + input_folder + "/" + "X_model1.npy")
    y = np.load("/app/" + input_folder + "/" + "y_model1.npy")

    return X, y

def model1(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=215)
    # def shuffle_split_data(X, y):
    #     np.random.seed(103)
    #     arr_rand = np.random.rand(X.shape[0])
    #     split = arr_rand < np.percentile(arr_rand, 80)

    #     X_train = X[split]
    #     y_train = y[split]
    #     X_test = X[~split]
    #     y_test = y[~split]

    #     return X_train, X_test, y_train, y_test
    # X_train, X_test, y_train, y_test = shuffle_split_data(X, y)

    # Create the model
    num_classes = len(np.unique(y_train))
    x_shape = X[0].shape

    model = models.Sequential([
        layers.Input(shape=(x_shape[0], x_shape[1])),  # Adjust the input shape based on your spectrogram size
        layers.Reshape(target_shape=(x_shape[0], x_shape[1], 1)),  # Add a channel dimension
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(x_shape[0], activation='relu'),
        layers.Dense(num_classes, activation='softmax') #sigmoid
    ])

    # Compile the model
    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    # Convert labels to one-hot encoding (assuming you have more than one class)
    y_train_encoded = tf.keras.utils.to_categorical(y_train, num_classes)
    y_test_encoded = tf.keras.utils.to_categorical(y_test, num_classes)
    

    # Train the model
    batch_size = 32
    epochs = 10

    history = model.fit(X_train, y_train_encoded, batch_size=batch_size, epochs=epochs, validation_split=0.1)


    # Evaluate the model on the test set
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test_encoded, axis=1)

    accuracy = accuracy_score(y_test_classes, y_pred_classes)
    print(f'Test accuracy: {accuracy:.2f}')

    # TODO: why was app used?
    # model.save("/app/" + output_folder + "/" + "model1_v1_vai.h5")
    model.save(output_folder + "/" + "model1_v1_vai.h5")

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
    model1(X, y)
    upload()


if __name__ == "__main__":
    main()

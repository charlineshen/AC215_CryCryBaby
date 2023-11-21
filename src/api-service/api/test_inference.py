# test inference.py by providing path to test audio file

import os
import sys
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from google.cloud import storage
from tempfile import TemporaryDirectory

# Call predict_self_host() from inference.py
from inference import predict_self_host

def test_inference():

    # define file
    file_path = "api/test_cry.wav"
    test_audio = "test_cry.wav"

    with TemporaryDirectory() as audio_dir:
        audio_path = os.path.join(audio_dir, test_audio)
        with open(file_path, "rb") as input_file:
            file_content = input_file.read()
        with open(audio_path, "wb") as output:
            output.write(file_content)

        # call predict_self_host() from inference.py
        prediction_results = predict_self_host(audio_path)
        
    print(prediction_results)


# define main function
if __name__ == "__main__":
    print("Current Working Directory:", os.getcwd())
    test_inference()

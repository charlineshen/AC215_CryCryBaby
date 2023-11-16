import requests
from flask import escape, request
import librosa
import numpy as np
import io

# TODO separate preprocessing into separate process
# TODO move to google cloud run if necessary
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

# TODO create a docker container using "container runtime"
# TODO abstract out the preprocessing code into a separate GCF instance

def receive_user_input(request):
    """
    Parses a .wav file from an HTTP request and sends it for prediction.
    """

    # Check for the right HTTP method
    if request.method == 'POST':
        
        # Assuming the WAV file is sent as a part of a multipart/form-data request
        if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.wav'):
                wav_data = file.read()

                # TODO check size of file
                # TODO can separate into separate GCF instance

                # Convert WAV data to spectrogram
                preprocessed_data = preprocess(wav_data)

                # Send for prediction
                final_response = get_prediction(preprocessed_data)

                # Return the response
                return final_response
        
    else:
        return 'Method not allowed', 405

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav'}

def preprocess(input_data):
    """
    Preprocesses the input data to be sent to the model.
    """

    # TODO add preprocessing code here
    spectrogram, sr = wav_to_spectrogram(input_data)

    return spectrogram

def get_prediction(input_data):
    # Preprocess data
    preprocessed_data = preprocess(input_data)

    # Call Model 1 (Cry/No Cry)
    model1_response = call_vertex_ai_model(model1_endpoint, preprocessed_data)
    cry_detected = interpret_model1_response(model1_response)

    # Initialize response object
    response = {
        "model1_prediction": model1_response,
        "model2_prediction": None
    }

    # If cry is detected, call Model 2
    if cry_detected:
        model2_response = call_vertex_ai_model(model2_endpoint, preprocessed_data)
        response["model2_prediction"] = model2_response

    return response

# Function to call a Vertex AI model endpoint
def call_vertex_ai_model(endpoint_url, data):
    # Add code to format the request, add authentication, and call the endpoint
    
    # Format request
    request_body = {
        "instances": data
    }

    # Add authentication
    # TODO add authentication

    # Call the endpoint
    response_from_vertex_ai = requests.post(endpoint_url, json=request_body)

    return response_from_vertex_ai

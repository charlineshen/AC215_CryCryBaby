from fastapi import FastAPI, UploadFile, File, HTTPException
import librosa
import numpy as np
import io
import requests

# Assuming other necessary imports and functions (like preprocess, get_prediction, etc.) remain the same

app = FastAPI()

# Define a route for receiving a .wav file
@app.post("/upload/")
async def receive_user_input(file: UploadFile = File(...)):
    # Check if the file is a .wav file
    if not file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Read file content
    contents = await file.read()

    # Convert to bytes buffer
    input_buffer = io.BytesIO(contents)

    # Preprocess and get prediction
    preprocessed_data = preprocess(input_buffer)
    response = get_prediction(preprocessed_data)

    return response

def wav_to_spectrogram(input_buffer, output_shape=(128, 64)):
    # Load the WAV file
    y, sr = librosa.load(input_buffer, sr=8000, dtype=np.float32)

    # Generate the spectrogram
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

    # Resize the spectrogram
    spectrogram = librosa.util.fix_length(spectrogram, size=output_shape[1], mode='constant', constant_values=0)

    # Normalize the spectrogram
    spectrogram = librosa.util.normalize(spectrogram)

    return spectrogram, sr

def preprocess(input_buffer):
    spectrogram, sr = wav_to_spectrogram(input_buffer)
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
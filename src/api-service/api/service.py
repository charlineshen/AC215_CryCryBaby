from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import asyncio
# from api.tracker import TrackerService
import pandas as pd
import os
from fastapi import File
from tempfile import TemporaryDirectory
from api import inference
from api import test_wav_upload
import numpy as np

# # Initialize Tracker Service
# tracker_service = TrackerService()

# Setup FastAPI app
app = FastAPI(title="API Server", description="API Server", version="v1")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    print("Startup tasks")
    # Start the tracker service
    # asyncio.create_task(tracker_service.track())


# Routes
@app.get("/")
async def get_index():
    return {"message": "Welcome to the API Service"}

@app.post("/predict")
async def predict(file: bytes = File(...)):
    print("service.py: predict file:", len(file), type(file))
    self_host_model = True

   # Save the audio
    with TemporaryDirectory() as audio_dir:
        audio_path = os.path.join(audio_dir, "audio.wav")
        with open(audio_path, "wb") as output:
            output.write(file)

        if self_host_model:
            prediction_results = inference.predict_self_host(audio_path)
        else:
            prediction_results = inference.predict_vertex_ai(audio_path)

    print("service.py: prediction_results")
    print(prediction_results)

    # Format the results
    converted_result = convert_and_format(prediction_results)

    return converted_result


# Make sure front-end container can send user input to API 
# upload_filepath is the location of uploaded file
@app.post("/testupload")
async def testupload(file: bytes = File(...)):
    # Save the audio
    with TemporaryDirectory() as audio_dir:
        audio_path = os.path.join(audio_dir, "audio1.wav")
        with open(audio_path, "wb") as output:
            output.write(file)

        upload_filepath = test_wav_upload.test_upload(audio_path)
    
    return upload_filepath

# Make sure front-end container can extract model output from API 
# We tweaked the dictionary format a bit for simplicity purposes
# the inference output should be like:
#   "cry": probability of cry 
#   "label": the winning label from model 2
#   "prob": the percentage of winning label
@app.get("/dummyoutputs")
async def dummy_outputs():
    return {"cry": 0.99,
            "label": "hungry",
            "prob": 0.98,}

def format_as_percentage(value):
    # Convert to standard Python float, multiply by 100, and round to 2 decimal places
    return round(float(value) * 100, 2)

def convert_and_format(data):
    if isinstance(data, dict):
        # Recursively apply conversion and formatting to each value in the dictionary
        return {k: convert_and_format(v) for k, v in data.items()}
    elif isinstance(data, np.float32):
        # Apply formatting to numpy.float32 values
        return format_as_percentage(data)
    return data

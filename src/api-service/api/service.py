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


# @app.get("/experiments")
# def experiments_fetch():
#     # Fetch experiments
#     df = pd.read_csv("/persistent/experiments/experiments.csv")

#     df["id"] = df.index
#     df = df.fillna("")

#     return df.to_dict("records")


# @app.get("/best_model")
# async def get_best_model():
#     model.check_model_change()
#     if model.best_model is None:
#         return {"message": "No model available to serve"}
#     else:
#         return {
#             "message": "Current model being served:" + model.best_model["model_name"],
#             "model_details": model.best_model,
#         }



@app.post("/predict")
async def predict(file: bytes = File(...)):
    print("service.py: predict file:", len(file), type(file))
    self_host_model = True

   # Save the audio
    with TemporaryDirectory() as audio_dir:
        audio_path = os.path.join(audio_dir, "audio.wav")
        with open(audio_path, "wb") as output:
            output.write(file)

        # # Make prediction
        # prediction_results = {"cry": 0.99,
        #                       "label": "hungry",
        #                       "prob": 0.98,}

        # TODO: call model to make prediction
        if self_host_model:
            # @Jessica
            prediction_results = inference.predict_self_host(audio_path)
        else:
            # @Adam
            prediction_results = inference.predict_vertex_ai(audio_path)

    print("service.py: prediction_results")
    print(prediction_results)

    # Fast-API won't accept numpy floats, must convert
    converted_result = convert_numpy_floats(prediction_results)

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

def convert_numpy_floats(data):
    # Input: dictionary
    # Output: dictionary with numpy floats converted to python floats
    if isinstance(data, dict):
        return {k: convert_numpy_floats(v) for k, v in data.items()}
    elif isinstance(data, np.float32):
        return float(data)
    return data

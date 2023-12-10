from fastapi import FastAPI, UploadFile, File

# create a FastAPI instance
app = FastAPI()

# define a route for receiving a .wav file
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    
    # TODO add preprocessing code here
    # Use container that returns a spectrogram

    # TODO add code to call the model endpoint
    # use manually uploaded models for now

    # TODO add code to interpret the response from the model

    # TODO add code to return the response


    
    
    
    return {"cry": .99,
            "no_cry": .01,
            "belly_pain": 0.01,
            "burping": 0.01,
            "discomfort": 0.01,
            "hungry": 0.96,
            "tired": 0.01}

from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"cry": .99,
            "no_cry": .01,
            "belly_pain": 0.01,
            "burping": 0.01,
            "discomfort": 0.01,
            "hungry": 0.96,
            "tired": 0.01}

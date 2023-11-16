from fastapi.testclient import TestClient
from test_api import app  # Assuming this is where your FastAPI app is defined
from io import BytesIO

client = TestClient(app)

def test_create_upload_file():
    with open("test_cry.wav", "rb") as file:
        response = client.post(
            "/uploadfile/",
            files={"file": ("test_cry.wav", file, "audio/wav")}
        )
        if response.status_code == 200:
            print("Success: Status code: 200")
        else: 
            print("Error: Status code: " + str(response.status_code))
        if response.json() == {"cry": .99,
            "no_cry": .01,
            "belly_pain": 0.01,
            "burping": 0.01,
            "discomfort": 0.01,
            "hungry": 0.96,
            "tired": 0.01}:
            print("Success: Response is correct")
        else:
            print("Error: Response is incorrect")

# Call the function to execute the test
test_create_upload_file()
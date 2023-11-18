import requests
import time

def test_create_upload_file():
    url = "http://test_api:8000/uploadfile/"
    files = {'file': ('test_cry.wav', open('test_cry.wav', 'rb'), 'audio/wav')}
    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(url, files=files)
            if response.status_code == 200:
                print("Success: Status code: 200")
                break
            else:
                print("Error: Status code: " + str(response.status_code))
        except requests.exceptions.ConnectionError as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(retry_delay)
        else:
            break  # Exit the loop if the request was successful

    else:  # Executed if the loop completed without breaking
        print("All retry attempts failed.")
        return  # Exit the function if all retries fail

    expected_response = {
        "cry": 0.99,
        "no_cry": 0.01,
        "belly_pain": 0.01,
        "burping": 0.01,
        "discomfort": 0.01,
        "hungry": 0.96,
        "tired": 0.01
    }

    if response.json() == expected_response:
        print("Success: Response is correct")
    else:
        print("Error: Response is incorrect")

if __name__ == "__main__":
    test_create_upload_file()

import os
import sys
import uuid
import base64
import requests

def send_image(image_path, server):
    # Read and encode image
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    image_id = str(uuid.uuid4())
    image = {"id": image_id, "image_data": image_data}
    # Send POST request to server
    response = requests.post(server, json=image)
    # Ensure correct response and return result
    if response.status_code == 200:
        object_detection = response.json()
        if object_detection.get('id') == image_id:
            return object_detection
        else:
            return "Error: Mismatch in image ID"
    else:
        return "Error: " + response

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <inputfolder> <endpoint>")
        sys.exit(1)

    input_folder = sys.argv[1]
    server = sys.argv[2]

    # Read images from folder
    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        print(send_image(image_path, server))

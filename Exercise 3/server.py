from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
import time

app = Flask(__name__)
app.json.sort_keys = False
PORT = 8080

# Variables for Average Inference Time
countImages = 0
runtime = 0
avgTime = 0

# Define paths for YOLO model
weights_path = "yolo_tiny_configs/yolov3-tiny.weights"
config_path = "yolo_tiny_configs/yolov3-tiny.cfg"
names_path = "yolo_tiny_configs/coco.names"

# Load object label names
labels = open(names_path).read().strip().split("\n")

# Load YOLO model
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]


#Define function for POST request
@app.route('/', methods=['POST'])
def detect_objects():
    t1_server = time.time()
    ## Average Inference Time Calculation
    global countImages
    countImages = countImages + 1
    ##
    start_time = time.time()

    #Get data from POST request and decode
    image_id = request.get_json().get('id')
    image_data = request.get_json().get('image_data')
    image = base64.b64decode(image_data)

    # Convert image to OpenCV format
    image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

    # Perform object detection with YOLO
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    # Process detections
    results = []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # At over 50% confidence add detection to results
            if confidence > 0.5:
                class_label = labels[class_id]
                results.append({"label": class_label, "accuracy": str(confidence)})

    ## Average Inference Time Calculation
    global runtime
    image_time = time.time() - start_time
    runtime = runtime + image_time
    global avgTime
    avgTime = runtime / countImages
    print("Average Inference Time: " + str(avgTime))

    with open("output\local_server_IT_Claudia.txt", "a") as f:
        f.write(f"{image_id}, {image_time}, {avgTime}\n")
    ##

    t2_server = time.time()
    # Transfer Time saved
    with open("output\local_server_TT_Claudia.txt", "a") as f:
        f.write(f"{image_id}, {t1_server}, {t2_server}\n")

    return jsonify({'id': image_id, 'objects': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
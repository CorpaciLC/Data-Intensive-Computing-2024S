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


@app.route('/', methods=['POST'])
def detect_objects():
    #Define function for POST request
    if request.method == 'POST':
        ## Average Inference Time Calculation
        global countImages
        countImages = countImages + 1
        ##

        #Get data from POST request and decode
        image_id = request.get_json().get('id')
        image_data = request.get_json().get('image_data')
        image = base64.b64decode(image_data)

        start_time = time.time()
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
        runtime = runtime + time.time() - start_time
        global avgTime
        avgTime = runtime / countImages
        print("Average Inference Time: " + str(avgTime))
        ##

        return jsonify({'id': image_id, 'objects': results})
    return jsonify({'error': 'Unsupported method'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
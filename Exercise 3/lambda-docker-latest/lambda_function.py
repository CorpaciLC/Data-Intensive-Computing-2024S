import boto3
import json
import cv2
import numpy as np
import time
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('yolo_results_dic2024s')

# Variables for Average Inference Time
countImages = 0
runtime = 0
avgTime = 0

def lambda_handler(event, context):
    global countImages, runtime, avgTime
    
    t1_server = time.time()  # Start measuring Lambda execution time
    
    # Load YOLO model and labels
    labels = open('/opt/coco.names').read().strip().split("\n")
    net = cv2.dnn.readNetFromDarknet('/opt/yolov3-tiny.cfg', '/opt/yolov3-tiny.weights')
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = unquote_plus(record['s3']['object']['key'])
        s3_url = f"s3://{s3_bucket}/{s3_key}"

        try:
            image_object = s3.get_object(Bucket=s3_bucket, Key=s3_key)
            image_content = image_object['Body'].read()
        except Exception as e:
            print(f"Error: {s3_key} from {s3_bucket}")
            raise e

        image = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_COLOR)
        
        countImages += 1  # Increment image count
        start_time = time.time()  # Start measuring inference time

        # YOLO
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)

        results = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    class_label = labels[class_id]
                    results.append({"label": class_label, "accuracy": str(confidence)})

        inference_time = time.time() - start_time  # Measure inference time

        # Update average inference time
        runtime += inference_time
        avgTime = runtime / countImages
        print(f"Average Inference Time: {avgTime}")

        # Log the inference time
        with open("/tmp/lambda_inference_time.txt", "a") as f:
            f.write(f"{s3_key}, {inference_time}, {avgTime}\n")
        
        # DynamoDB
        table.put_item(
            Item={
                'ImageURL': s3_url,
                'DetectedObjects': results
            }
        )

    t2_server = time.time()  # End measuring Lambda execution time
    
    # Log the execution time
    with open("/tmp/lambda_execution_time.txt", "a") as f:
        f.write(f"{s3_key}, {t1_server}, {t2_server}\n")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Completed and stored in DynamoDB.')
    }

import boto3
import json
import cv2
import numpy as np
import time
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
results_table = dynamodb.Table('yolo_results_dic2024s')
timings_table = dynamodb.Table('timings_table_dic2024s')

def lambda_handler(event, context):
    for record in event['Records']:
        # t2_client = time.time()
        
        # Load YOLO model and labels
        labels = open('/opt/yolo_tiny_configs/coco.names').read().strip().split("\n")
        net = cv2.dnn.readNetFromDarknet('/opt/yolo_tiny_configs/yolov3-tiny.cfg', '/opt/yolo_tiny_configs/yolov3-tiny.weights')
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        s3_bucket = record['s3']['bucket']['name']
        s3_key = unquote_plus(record['s3']['object']['key'])
        try:
            image_object = s3.get_object(Bucket=s3_bucket, Key=s3_key)
            image_content = image_object['Body'].read()
        except Exception as e:
            print(f"Error: {s3_key} from {s3_bucket}")
            raise e

        image = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_COLOR)
        
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
        print(f"Inference Time: {inference_time}")

        t2_server = time.time()  # End measuring Lambda execution time

        results_table.put_item(
            Item={
                'ImageID': s3_key, 
                'DetectedObjects': results
            }
        )


        timings_table.put_item(
            Item={
                'ImageID': s3_key,
                'InferenceTime': str(inference_time),
                # 't2_client': str(t2_client),
                't2_server': str(t2_server)
            }
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Completed and stored in DynamoDB.')
    }

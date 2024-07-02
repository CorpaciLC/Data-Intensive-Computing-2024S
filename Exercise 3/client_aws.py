import os
import sys
import uuid
import boto3
import time

def upload_image_to_s3(image_path, bucket_name):
    s3 = boto3.client('s3')
    image_id = str(uuid.uuid4())
    
    t1_client = time.time()  # Start measuring client transfer time
    s3.upload_file(image_path, bucket_name, image_id)
    t2_client = time.time()  # End measuring client transfer time
    
    with open("output/aws_client_TT.txt", "a") as f:
        f.write(f"{image_id}, {t1_client}, {t2_client}\n")

    return image_id

def get_lambda_processing_time(image_id):
    # Implement a method to retrieve Lambda processing time, e.g., from logs or a database
    # This is a placeholder implementation.
    lambda_processing_time = 0.5  # Replace with actual logic
    return lambda_processing_time

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <inputfolder> <bucket>")
        sys.exit(1)

    input_folder = sys.argv[1]
    bucket_name = sys.argv[2]

    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        image_id = upload_image_to_s3(image_path, bucket_name)
        print(f"Uploaded {filename} as {image_id}")

        # Measure and log the Lambda processing time
        lambda_processing_time = get_lambda_processing_time(image_id)
        with open("output/aws_lambda_processing_time.txt", "a") as f:
            f.write(f"{image_id}, {lambda_processing_time}\n")

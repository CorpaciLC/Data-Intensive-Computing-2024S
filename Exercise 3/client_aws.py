import os
import sys
import uuid
import boto3

def upload_image_to_s3(image_path, bucket_name):
    s3 = boto3.client('s3')
    image_id = str(uuid.uuid4())
    s3.upload_file(image_path, bucket_name, image_id)
    return image_id

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

import os
import sys
import uuid
import boto3
import time
import pandas as pd

def upload_image_to_s3(image_path, bucket_name):
    '''
    Upload an image to an S3 bucket and return the image ID'''
    s3 = boto3.client('s3')
    image_id = str(uuid.uuid4())
    
    t1_client = time.time()  # Start measuring client transfer time
    s3.upload_file(image_path, bucket_name, image_id)
    t1_server = time.time()  # End measuring client transfer time
    
    with open("output/aws_t1.txt", "a") as f:
        f.write(f"{image_id}, {t1_client}, {t1_server}\n")

    return image_id


def get_timings(image_id):
    '''
    Retrieve the Lambda processing time from the DynamoDB table'''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('timings_table_dic2024s') 
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('ImageID').eq(image_id)
    )
    
    timeout = 20 # Timeout in seconds
    timeout_time = time.time()
    while time.time() - timeout_time < timeout:
        time.sleep(1)
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('ImageID').eq(image_id)
        )
        if response['Items']:
            timings = response['Items'][0]
            t2_server = float(timings['t2_server'])
            print(f"Lambda processing time for ImageID {image_id}.")
            return t2_server
    else:
        print(f"Timeout: No timings found for ImageID {image_id} within {timeout} seconds")
        return -1

def get_results(image_id):
    '''
    Retrieve the Lambda results from the DynamoDB table'''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yolo_results_dic2024s') 
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('ImageID').eq(image_id)
    )
    
    timeout = 20 # Timeout in seconds
    timeout_time = time.time()
    while time.time() - timeout_time < timeout:
        time.sleep(1)
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('ImageID').eq(image_id)
        )
        if response['Items']:
            print(f"Accessed image with id={image_id}")
            return True
    else:
        print(f"Timeout: No timings found for ImageID {image_id} within {timeout} seconds")
        return False



def export_table_to_csv(table_name):
    '''
    Export the DynamoDB table to a CSV file
    '''
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)

    response = table.scan()
    data = response['Items']
    df = pd.DataFrame(data)
    df.to_csv(f'output\\{table_name}.csv', index=False)
    print(f"Data exported successfully to {table_name}.csv")


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
        if get_results(image_id):
            t2_client = time.time()
            t2_server = get_timings(image_id)
            with open("output/aws_t2.txt", "a") as f:
                f.write(f"{image_id}, {t2_client}, {t2_server}\n")


    export_table_to_csv('yolo_results_dic2024s')
    export_table_to_csv('timings_table_dic2024s')






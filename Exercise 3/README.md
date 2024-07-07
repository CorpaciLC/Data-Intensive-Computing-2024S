# Local 

## Prerequisites
- Needs yolo_tiny_configs folder with files from TUWEL

## Steps
Start server.py

Run on data with:
python .\client.py <inputfolder> <endpoint>

python .\client.py .\input_folder_small\ http://localhost:8080


# AWS Lambda with Docker and YOLO Configuration

This guide describes the steps to set up and deploy an AWS Lambda function with Docker, including the necessary YOLO configuration files and dependencies (OpenCV, NumPy, and boto3). The Lambda function will be stored in Amazon Elastic Container Registry (ECR) and will process images for object detection, storing results in DynamoDB.

## Prerequisites

- AWS CLI configured with appropriate permissions
- Docker installed and running
- AWS account ID
- YOLO configuration files (`coco.names`, `yolov3-tiny.cfg`, `yolov3-tiny.weights`) stored in an S3 bucket

## Steps

### 0. Setup
From aws academy -> Launch AWS Academy Learner Lab -> aws details -> copy contents of aws cli to ~/.aws/credentials and save

### 1. Prepare YOLO Configuration Files and store them to an S3 bucket

### 2. Create a Dockerfile

Create a `Dockerfile` with the following content to set up the environment for the Lambda function:

```dockerfile
FROM public.ecr.aws/lambda/python:3.11
RUN pip install numpy opencv-python-headless boto3

# Copy YOLO config files from S3 bucket
COPY yolo_tiny_configs /opt/yolo_tiny_configs

# Copy lambda function
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.lambda_handler"]
```

### 3. Build Docker Image
```
docker build -t lambda-docker .
```

### 4. Login to AWS ECR
Change \<region\> and <aws_account_id> accordingly
```
aws ecr get-login-password --region <region>| docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

### 5. Create ECR Repository
```
aws ecr create-repository --repository-name lambda-docker
```

### 6. Tag and Push Docker Image to ECR
```
docker tag lambda_docker:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/lambda-docker:latest
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/lambda-docker:latest

```
### 7. Create Lambda Function and Deploy
7.1 Go to the AWS Lambda console and choose "Create Function"

7.2 Choose container image as the function type and select image from ECR repo

7.3 Configure the function. Set memory to 1024MB and timeout=10s

7.4 Add S3 bucket trigger for all create-events.

### 9. Explore results and timings

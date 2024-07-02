# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Install dependencies
RUN pip install numpy opencv-python-headless

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["lambda_function.lambda_handler"]

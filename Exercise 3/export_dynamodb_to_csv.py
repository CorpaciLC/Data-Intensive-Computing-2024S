import boto3
import pandas as pd

# Initialize DynamoDB resource using the default session
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Replace 'yolo_results_dic2024s' with your DynamoDB table name
table = dynamodb.Table('yolo_results_dic2024s')

# Scan the entire table
response = table.scan()
data = response['Items']

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Normalize the nested JSON data for 'DetectedObjects'
df = df.explode('DetectedObjects').reset_index(drop=True)
detected_objects = pd.json_normalize(df['DetectedObjects'])
df = df.drop(columns=['DetectedObjects']).join(detected_objects)

# Save the DataFrame to a CSV file
df.to_csv('output\\dynamodb_export.csv', index=False)
print("Data exported successfully to dynamodb_export.csv")

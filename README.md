# Data Intensive Computing - 2024S

## Exercise 2. Large Text Corpora Processing

[Overleaf project](httpswww.overleaf.com2915981151zzqyhfznckzc#dcbaeb)

**Dataset**: Amazon Review Dataset


### Tasks

#### Part 1. RDDs
Calculate chi-square values, output the sorted top terms per category, and write the results to `output_rdd.txt`.

#### Part 2. DatasetsDataFrames - SparkML and Pipelines
Convert review texts to a TFIDF-weighted feature vector representation using the Spark DataFrame/Dataset API. Build a transformation pipeline and output the selected terms to `output_ds.txt`.

#### Part 3. Text Classification
Extend the pipeline from Part 2 to train a Support Vector Machine (SVM) classifier. Perform parameter optimization using grid search and evaluate the model using the MulticlassClassificationEvaluator.



## Exercise 3. Computational Offloading of Object Detection Services -

[Overleaf project](https://www.overleaf.com/8111393219zrkvpgvxspxp#b00c71)

**Dataset**: [COCO (Common Objects in Context Dataset)](http://cocodataset.org/#home)


### Tasks

#### Part 1. Local Implementation
Develop a RESTful API using Flask to upload images and perform object detection using the YOLO model. The service should accept base64-encoded images in JSON format, process them locally, and return the detected objects in a JSON response.

#### Part 2. Remote Cloud Implementation
Set up an AWS infrastructure to offload image processing tasks. Implement an image upload mechanism to S3, trigger a Lambda function for object detection upon upload, and store the results in DynamoDB. Modify the local YOLO script to work within the Lambda environment.



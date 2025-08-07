import boto3
from boto3.dynamodb.conditions import Attr
from dotenv import load_dotenv
import os

import json

#Load .env file
load_dotenv()

#Access values
region = os.getenv('REGION')
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')

dataJsons_bucket = os.getenv('BUCKET_NAME')
modelList_table = os.getenv('ITEMS_TO_SEARCH')

#DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name= region,
    aws_access_key_id= access_key,
    aws_secret_access_key= secret_key
)

s3 = boto3.client(
    's3',
    region_name= region,
    aws_access_key_id= access_key,
    aws_secret_access_key= secret_key
)

#Tables and global values
modelList = dynamodb.Table(modelList_table)

#get list of models
response = modelList.scan(FilterExpression=Attr('ACTIVE').eq(True))
targets = response['Items']
model_names = sorted({target['Model'].upper() for target in targets})

data = json.dumps(model_names, indent=2)

s3.put_object(
    Bucket = dataJsons_bucket,
    Key = 'data/models.json',
    Body = data,
    ContentType = 'application/json'
)

print("✅ models.json uploaded to S3!")
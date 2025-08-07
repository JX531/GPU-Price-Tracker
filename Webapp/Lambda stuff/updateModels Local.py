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

modelList_table = os.getenv('ITEMS_TO_SEARCH')

#DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
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

#update models.json
os.makedirs('Webapp/frontend-gpu-price-tracker/public/data', exist_ok=True)
with open('Webapp/frontend-gpu-price-tracker/public/data/models.json', 'w') as f:
    json.dump(model_names, f, indent=2)

    
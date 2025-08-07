import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
import os

from datetime import datetime
from zoneinfo import ZoneInfo
import json

#Load .env file
load_dotenv()

#Access values
region = os.getenv('REGION')
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')

#DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name= region,
    aws_access_key_id= access_key,
    aws_secret_access_key= secret_key
)

#S3
s3 = boto3.client(
    's3',
    region_name= region,
    aws_access_key_id= access_key,
    aws_secret_access_key= secret_key
)

#Tables and global values
tableDaily = dynamodb.Table(os.getenv('DAILY_AVERAGES_TABLE'))
cheapestDaily = dynamodb.Table(os.getenv("DAILY_CHEAPEST"))
dataJsons_bucket = os.getenv('BUCKET_NAME')

# def transformData(raw_data):
#     transformed = {}
#     for entry in raw_data:
#         date = entry["Date"]
#         transformed[date] = {
#             "AvgPrice": entry["AvgPrice"],
#             "NumListings": int(entry["NumListings"]),
#             "Model": entry["Model"]
#         }
#     return transformed

#Decimal to float encoder
from decimal import Decimal
class DecimalToFloat(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

#Get list of models
response = s3.get_object(Bucket = dataJsons_bucket, Key = "data/models.json")
models = json.load(response['Body'])

#Get last updated dates
lastUpdated = {}
try:
    response = s3.get_object(Bucket = dataJsons_bucket, Key = "data/lastUpdated.json")
    lastUpdated = json.load(response['Body'])
except:
    print("lastUpdated.json not present, creating it...")

#Scan for each model and update its json
Today = datetime.now(ZoneInfo("Asia/Singapore")).strftime("%Y-%m-%d") #today date, using SG timezone
for model in models:
    lastUpdatedDate = lastUpdated.get(model, None)
    modelFilePath = f"data/{model}.json"

    #Only pull missing data
    if lastUpdatedDate:
        response = s3.get_object(Bucket = dataJsons_bucket, Key = modelFilePath) #pull existing data from S3
        curData = json.load(response['Body'])

        response = tableDaily.query(KeyConditionExpression=Key('Model').eq(model) & Key('Date').gt(lastUpdatedDate)) #query for matching model with date greater than last updated
        items = response['Items']

        data = curData + items #add new items to current data
    
    #Pull all
    else:   
        response = tableDaily.query(KeyConditionExpression=Key('Model').eq(model)) #query for matching model
        data = response['Items']
    
    #Push to its relevant json on S3
    data.sort(key=lambda x: x['Date']) #sort by date
    modelData = json.dumps(data, indent=2, cls= DecimalToFloat)
    s3.put_object(
        Bucket = dataJsons_bucket,
        Key = modelFilePath,
        Body = modelData,
        ContentType = 'application/json'
    )

    #Update model's lastUpdated date
    lastUpdated[model] = Today

#Update lastUpdated json on S3
lastUpdatedData = json.dumps(lastUpdated, indent=2)
s3.put_object(
        Bucket = dataJsons_bucket,
        Key = "data/lastUpdated.json",
        Body = lastUpdatedData,
        ContentType = 'application/json'
    )


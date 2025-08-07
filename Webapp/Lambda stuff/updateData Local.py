import boto3
from boto3.dynamodb.conditions import Attr
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


#Tables and global values
tableDaily = dynamodb.Table(os.getenv('DAILY_AVERAGES_TABLE'))
cheapestDaily = dynamodb.Table(os.getenv("DAILY_CHEAPEST"))

#decimal to float encoder
from decimal import Decimal
class DecimalToFloat(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

#get list of models
os.makedirs('Webapp/frontend-gpu-price-tracker/public/data', exist_ok=True)
with open('Webapp/frontend-gpu-price-tracker/public/data/models.json', 'r') as f:
    models = json.load(f) 

#get last updated dates
lastUpdated = {}
try:
    with open('Webapp/frontend-gpu-price-tracker/public/data/lastUpdated.json', 'r') as f:
        lastUpdated = json.load(f)
except:
    print("lastUpdated.json not found, creating it...")

#scan for each model and update its json
Today = datetime.now(ZoneInfo("Asia/Singapore")).strftime("%Y-%m-%d") #today date, using SG timezone
for model in models:
    lastUpdatedDate = lastUpdated.get(model, None)
    filePath = f'Webapp/frontend-gpu-price-tracker/public/data/{model}.json'

    #only need to update missing dates
    if lastUpdatedDate:
        #existing data
        with open(filePath,'r') as f:
            curData = json.load(f)
        
        #get new data and append to current data
        response = tableDaily.scan(FilterExpression=Attr('Model').eq(model) & Attr('Date').gt(lastUpdatedDate))
        items = response['Items']
        data = curData + items

    #pull all
    else:
        response = tableDaily.scan(FilterExpression=Attr('Model').eq(model))
        data = response['Items']

    #dump to json
    data.sort(key=lambda x: x['Date'])
    with open(filePath, 'w') as f:
        json.dump(data, f, indent=2, cls= DecimalToFloat)
    
    #update lastUpdated
    lastUpdated[model] = Today

#update lastUpdated json
with open('Webapp/frontend-gpu-price-tracker/public/data/lastUpdated.json', 'w') as f:
        json.dump(lastUpdated, f, indent=2)


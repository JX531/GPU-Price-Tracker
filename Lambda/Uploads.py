from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import os
import boto3
import json

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#DynamoDB
dynamodb = boto3.resource('dynamodb')

#S3
s3 = boto3.client('s3')

#Bucket
S3Bucket = os.environ['S3_BUCKET']

#Tables
cheapestDaily = dynamodb.Table(os.environ['DAILY_CHEAPEST_TABLE'])

#Decimal to float encoder for jsons
class DecimalToFloat(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def uploadDailyAverage(Model, dailyModelData, Today):
    '''
    Uploads the average price of a model for the day to the relevant S3 Json file
    Input :
    Model - String, which model you are uploading for e.g "RTX 5070 TI"
    dailyModelData - Array of objects containing product data, from functions in Amazon.py scraper,
                    each dailyModelData entry has 'Model', 'Brand', 'VRAM', 'Price', 'Date', 'Link', 'Title'
    Today - String, date of today

    Output : None
    '''

    NumListings = len(dailyModelData) #find number of listings

    if NumListings == 0: #no data today
        logger.info(f"No Data for {Model} on {Today}")
        return

    else:
        AvgPrice = float(str(round(sum(item["Price"] for item in dailyModelData) / NumListings, 2))) #calculate average price, converted to decimal for dynamoDB

    #Update S3 Json
    try: 
        #Pull existing data from S3
        try:
            response = s3.get_object(Bucket = S3Bucket, Key = f"data/{Model}.json")
            existingData = json.load(response['Body'])
        
        except Exception as e:
            if "NoSuchKey" in str(e):
                logger.info(f"Creating new file for {Model}")
                existingData = {}
            else:
                logger.error(f"S3 get failed for {Model} on {Today}: {str(e)}")

        #Update / add today's entry
        existingData[Today] = {
            'NumListings': NumListings,
            "AvgPrice" : AvgPrice,
            "Model": Model
        }
        
        #Encode back to Json
        updatedData = json.dumps(existingData, indent=2, cls= DecimalToFloat)

        #Push updated data back to S3
        s3.put_object(
            Bucket = S3Bucket,
            Key = f"data/{Model}.json",
            Body = updatedData,
            ContentType = 'application/json',
            CacheControl='max-age=86400'  #24h cache
        )

        logger.info(f"Uploaded average for {Model} on {Today}, averaging at {AvgPrice} across {NumListings} Listings")

    except Exception as e:
        logger.error(f"Failed to upload daily average for {Model} on {Today}: {str(e)}")


def uploadRawListings(Model, dailyModelData, Today):
    '''
    Uploads the cheapest 3 listings for the model for today to DynamoDB table
    Input :
    Model - String, which model you are uploading for e.g "RTX 5070 TI"
    daikyModelData - Array of objects containing product data, from functions in Amazon.py scraper,
                    each dailyModelData entry has 'Model', 'Brand', 'VRAM', 'Price', 'Date', 'Link', 'Title'
    Today - String, date of today

    Output : None
    '''
    NumListings = len(dailyModelData) #find number of listings

    if NumListings == 0: #no data today
        logger.info(f"No Data for {Model} on {Today}")
        return 
    
    else:
        dailyModelData.sort(key=lambda item: item["Price"]) #Sort by Price, ascending
        cheapest3 = dailyModelData[:3] #slice the cheapest 3 from array
        expiry = int(datetime.now(ZoneInfo("Asia/Singapore")).timestamp()) + (24 * 3600) #calculate TTL, using SG timezone

        try: #upload with batch writer
            with cheapestDaily.batch_writer() as batch:
                for item in cheapest3:
                    batch.put_item(
                        Item={
                            'Model': Model,
                            'Brand': item['Brand'],
                            'VRAM': item['VRAM'],
                            'Price': Decimal(str(item['Price'])),
                            'DateLink': '#'.join([Today, item['Link']]),
                            'Title': item['Title'][:500],
                            'Expiry': expiry
                        }
                    )
            logger.info(f"Uploaded cheapest 3 listings for {cheapest3[0]['Model']} on {Today}")

        except Exception as e:
            logger.error(f"Error uploading raw listings for {Model} on {Today}: {e}")

from Amazon import findProduct
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import boto3
from boto3.dynamodb.conditions import Attr
from dotenv import load_dotenv
import os

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
scrapeTargets = dynamodb.Table(os.getenv('ITEMS_TO_SEARCH'))


def uploadDailyAverage(Model, dailyModelData, Today):
    NumListings = len(dailyModelData)

    if NumListings == 0:
        print(f"No Data for {Model} on {Today}")
        return

    else:
        AvgPrice = Decimal(str(round(sum(item["Price"] for item in dailyModelData) / NumListings, 2)))

    try:
        tableDaily.put_item(
            Item={
                'Model': Model,
                'Date': Today,
                'NumListings': NumListings,
                'AvgPrice': AvgPrice
            }
        )

        print(f"Uploaded average for {Model} on {Today}, averaging at {AvgPrice} across {NumListings} Listings")

    except Exception as e:
        print(f"Failed to upload daily average for {Model} on {Today}: {str(e)}")


#'Model', 'Brand', 'VRAM', 'Price', 'Date', 'Link', 'Title'
def uploadRawListings(Model, dailyModelData, Today):
    NumListings = len(dailyModelData)

    if NumListings == 0:
        print(f"No Data for {Model} on {Today}")
        return 
    
    else:
        dailyModelData.sort(key=lambda item: item["Price"])
        cheapest3 = dailyModelData[:3]
        expiry = int(datetime.today().timestamp()) + (24 * 3600)

        print(cheapest3)

        try:
            with cheapestDaily.batch_writer() as batch:
                for item in cheapest3:
                    batch.put_item(
                        Item={
                            'Model': Model,
                            'Brand': item['Brand'],
                            'VRAM': item['VRAM'],
                            'Price': Decimal(str(item['Price'])),
                            'DateLink': '#'.join([Today, item['Link']]),
                            'Title': item['Title'],
                            'Expiry': expiry
                        }
                    )
            print(f"Uploaded cheapest 3 listings for {cheapest3[0]['Model']} on {Today}")

        except Exception as e:
            print(f"Error uploading raw listings for {Model} on {Today}: {e}")


def routine():
    Today = datetime.today().strftime("%Y-%m-%d")
    response = scrapeTargets.scan(FilterExpression=Attr('ACTIVE').eq(True))
    targets = response['Items']

    for target in targets:
        targetModel = target['Model'].upper()
        data = findProduct(targetModel)
        # uploadDailyAverage(targetModel, data, Today)
        # uploadRawListings(targetModel, data, Today)


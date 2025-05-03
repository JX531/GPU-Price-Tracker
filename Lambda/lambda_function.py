from Amazon import findProduct
from datetime import datetime
from decimal import Decimal
import os
import boto3
from boto3.dynamodb.conditions import Attr

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#DynamoDB
dynamodb = boto3.resource('dynamodb')

#Tables
tableDaily = dynamodb.Table(os.environ['DAILY_AVERAGES_TABLE'])
cheapestDaily = dynamodb.Table(os.environ['DAILY_CHEAPEST_TABLE'])
scrapeTargets = dynamodb.Table(os.environ['ITEMS_TO_SEARCH_TABLE'])


def uploadDailyAverage(Model, dailyModelData, Today):
    NumListings = len(dailyModelData)

    if NumListings == 0:
        logger.info(f"No Data for {Model} on {Today}")
        AvgPrice = Decimal(0)

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

        logger.info(f"Uploaded average for {Model} on {Today}, averaging at {AvgPrice} across {NumListings} Listings")

    except Exception as e:
        logger.error(f"Failed to upload daily average for {Model} on {Today}: {str(e)}")


#'Model', 'Brand', 'VRAM', 'Price', 'Date', 'Link', 'Title'
def uploadRawListings(Model, dailyModelData, Today):
    NumListings = len(dailyModelData)

    if NumListings == 0:
        logger.info(f"No Data for {Model} on {Today}")
        return 
    
    else:
        dailyModelData.sort(key=lambda item: item["Price"])
        cheapest3 = dailyModelData[:3]
        expiry = int(datetime.today().timestamp()) + (24 * 3600)

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
            logger.info(f"Uploaded cheapest 3 listings for {cheapest3[0]['Model']} on {Today}")

        except Exception as e:
            logger.error(f"Error uploading raw listings for {Model} on {Today}: {e}")


def lambda_handler(event, context):
    Today = datetime.today().strftime("%Y-%m-%d")

    try:
        response = scrapeTargets.scan(FilterExpression=Attr('ACTIVE').eq(True))
        targets = response['Items']
    except Exception as e:
        logger.error(f"Failed to fetch scrape targets: {str(e)}")
        return {"status": "failed", "error": "Target scan failed"}

    for target in targets:
        try:
            targetModel = target['Model'].upper()
            data = findProduct(targetModel)
            uploadDailyAverage(targetModel, data, Today)
            uploadRawListings(targetModel, data, Today)

        except Exception as e:
            logger.error(f"Error for {target['Model']} on {Today}: {str(e)}")
            continue 
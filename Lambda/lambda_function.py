from Amazon import findProduct
from datetime import datetime
from zoneinfo import ZoneInfo
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
    '''
    Uploads the average price of a model for the day to the relevant DynamoDB table
    Input :
    Model - String, which model you are uploading for e.g "RTX 5070 TI"
    daikyModelData - Array of objects containing product data, from functions in Amazon.py scraper
    Today - String, date of today

    Output : None
    '''

    NumListings = len(dailyModelData) #find number of listings

    if NumListings == 0: #no data today
        logger.info(f"No Data for {Model} on {Today}")
        return

    else:
        AvgPrice = Decimal(str(round(sum(item["Price"] for item in dailyModelData) / NumListings, 2))) #calculate average price, converted to decimal for dynamoDB

    try: #upload to dynamoDB
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
    '''
    Uploads the cheapest 3 listings for the model for today
    Input :
    Model - String, which model you are uploading for e.g "RTX 5070 TI"
    daikyModelData - Array of objects containing product data, from functions in Amazon.py scraper
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
                            'Title': item['Title'],
                            'Expiry': expiry
                        }
                    )
            logger.info(f"Uploaded cheapest 3 listings for {cheapest3[0]['Model']} on {Today}")

        except Exception as e:
            logger.error(f"Error uploading raw listings for {Model} on {Today}: {e}")


def lambda_handler(event, context):
    Today = datetime.now(ZoneInfo("Asia/Singapore")).strftime("%Y-%m-%d") #today date, using SG timezone

    try:
        #get targets to scrape from DynamoDB table e.g "RTX 5070 TI"
        response = scrapeTargets.scan(FilterExpression=Attr('ACTIVE').eq(True)) 
        targets = response['Items']
    except Exception as e:
        logger.error(f"Failed to fetch scrape targets: {str(e)}")
        return {"status": "failed", "error": "Target scan failed"}

    #proceed to scrape for each target
    for target in targets:
        try:
            targetModel = target['Model'].upper() #Get the Model we are scraping for
            data = findProduct(targetModel) #Scrape for it

            #upload the data
            uploadDailyAverage(targetModel, data, Today)
            uploadRawListings(targetModel, data, Today)

        except Exception as e:
            logger.error(f"Error for {target['Model']} on {Today}: {str(e)}")
            continue 
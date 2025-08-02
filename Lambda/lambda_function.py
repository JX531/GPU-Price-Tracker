from Amazon import findProduct
from Uploads import uploadDailyAverage, uploadRawListings
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import boto3
from boto3.dynamodb.conditions import Attr

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#DynamoDB
dynamodb = boto3.resource('dynamodb')

#Tables
scrapeTargets = dynamodb.Table(os.environ['ITEMS_TO_SEARCH_TABLE'])


def lambda_handler(event, context):
    '''
    Function for lamba, input parameters are not used
    Cloudwatch Eventbridge triggers this function at least once a day. 
    '''
    Today = datetime.now(ZoneInfo("Asia/Singapore")).strftime("%Y-%m-%d") #today date, using SG timezone

    try:
        #get targets to scrape from S3 Json e.g "RTX 5070 TI"
        response = scrapeTargets.scan(FilterExpression=Attr('ACTIVE').eq(True)) 
        
    except Exception as e:
        logger.error(f"Failed to fetch scrape targets: {str(e)}")
        return {"status": "failed", "error": "Target scan failed"}

    #proceed to scrape for each target
    for target in response['Items']:
        try:
            targetModel = target['Model'].upper() #Get the Model we are scraping for
            data = findProduct(targetModel) #Scrape for it

            #upload the data
            uploadDailyAverage(targetModel, data, Today)
            uploadRawListings(targetModel, data, Today)

        except Exception as e:
            logger.error(f"Error for {target['Model']} on {Today}: {str(e)}")
            continue 
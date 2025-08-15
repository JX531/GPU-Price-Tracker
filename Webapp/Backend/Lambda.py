import json
from decimal import Decimal
import os
import boto3
from boto3.dynamodb.conditions import Key

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#DynamoDB
dynamodb = boto3.resource('dynamodb')

#Tables
userAlerts = dynamodb.Table(os.environ['User_Alerts'])

#Decimal to float encoder for jsons
class DecimalToFloat(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)
    
def lambda_handler(event, context):
    method = event['httpMethod']

    if method == "GET": #get all entries for a given user
        try:
            UserEmail = event.get("queryStringParameters", {}).get("UserEmail", None)
            if not UserEmail:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps("Missing UserEmail parameter")
                }
        
            response = userAlerts.query(KeyConditionExpression=Key("UserEmail").eq(UserEmail))
            data = [{"Model": item["Model"], "Price": item["Price"]} for item in response.get('Items', [])]
            return {
                "statusCode" : 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(data, cls=DecimalToFloat)
            }
        
        except Exception as e:
            logger.error(f"Failed {method}: {e}")
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(str(e))
            }

    elif method == "POST" or method == "PUT":
        try:
            body = json.loads(event['body'])
            UserEmail = body.get("UserEmail", None)
            Model = body.get("Model", None)
            Price = body.get("Price", None)

            if UserEmail and Model and Price:
                userAlerts.put_item(
                Item={
                    "UserEmail": UserEmail,
                    "Model": Model,
                    "Price": Decimal(str(Price))
                })

                return {
                    "statusCode" : 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps(f"Successful {method} for {UserEmail}'s {Model} at ${Price}")
                }

            else:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps("Missing UserEmail or Model or Price parameter")
                }

        except Exception as e:
            logger.error(f"Failed {method}: {e}")
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(str(e))
            }
        
    elif method == "DELETE":
        try:
            body = json.loads(event['body'])
            UserEmail = body.get("UserEmail", None)
            Model = body.get("Model", None)

            if UserEmail and Model:
                userAlerts.delete_item(
                    Key={'UserEmail': UserEmail, "Model": Model}
                )

                return {
                    "statusCode" : 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps(f"Successful {method} for {UserEmail}'s {Model}")
                }

            else:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps("Missing UserEmail or Model parameter")
                }

        except Exception as e:
            logger.error(f"Failed {method}: {e}")
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(str(e))
            }

    else:
        return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps("Invalid Method")
            }
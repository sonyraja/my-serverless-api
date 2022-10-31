import os
import boto3
import logging
import traceback
import sys
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handler(event, context):
    """
    Lambda handler function to be triggered by findProduct API.
    """
    try:
        productId = event['pathParameters']['id']

        logger.debug("Product Id: %s", productId)

        logger.info("Finding product...")
        client = boto3.client('dynamodb')
        response = client.get_item(
                            TableName=os.environ['DYNAMODB_TABLE'],
                            Key={
                                    'id': {
                                        'S': productId
                                    }
                                })
        logger.info("Success: %s", response)
        returnResp = {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": json.dumps(response)
        }
        return returnResp
    except Exception as e:
        logger.error("Unknow exception occured when finding product. %s", e)
        traceback.print_exc()
        sys.exit()
        returnResp = {
            "isBase64Encoded": True,
            "statusCode": 500,
            "body": "Error occured when finding product"
        }
        return returnResp

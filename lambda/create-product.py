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
    Lambda handler function to be triggered by saveProduct API.
    """
    try:
        requestJson = json.loads(event["body"])
        productId = requestJson['id']
        title = requestJson['title']
        description = requestJson['description']
        price = requestJson['price']

        logger.debug("Product Id: %s", productId)
        logger.debug("Product Title: %s", title)
        logger.debug("Product Description: %s", description)
        logger.debug("Product Price: %s", price)
        logger.debug("DynamoDB Table: %s", os.environ['DYNAMODB_TABLE'])

        logger.info("Saving product...")
        client = boto3.client('dynamodb')
        response = client.put_item(
                            TableName=os.environ['DYNAMODB_TABLE'],
                            Item={
                                    'id': {
                                        'S': productId
                                    },
                                    'title': {
                                        'S': title
                                    },
                                    'description': {
                                        'S': description
                                    },
                                    'price': {
                                        'N': price
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
        logger.error("Unknow exception occured when saving product. %s", e)
        traceback.print_exc()
        returnResp = {
            "isBase64Encoded": True,
            "statusCode": 500,
            "body": "Error occured when creating product"
        }
        return returnResp
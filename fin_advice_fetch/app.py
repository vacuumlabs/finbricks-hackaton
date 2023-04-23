import json
import os

import boto3 as boto3

TABLE_NAME = 'finbricks-hackaton-DynamoDBTable-1C7A3ZJGAMF6V'
REGION_NAME = 'eu-central-1'


def lambda_handler(event, context):
    print(event)
    query_parameters = event.get("queryStringParameters", {})
    client_id = query_parameters.get("clientId", "")

    dynamodb_config = {
        'region_name': REGION_NAME
    }

    try:
        dynamodb = boto3.resource('dynamodb', **dynamodb_config)
        table = dynamodb.Table(TABLE_NAME)
        fetch = table.get_item(
            Key={
                'id': client_id
            }
        )
        response = {"status": "success", "data": fetch['Item']}
    except:
        response = {"status": "error", "data": {}}

    print(response)
    # return response
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_1_event.json")), None))

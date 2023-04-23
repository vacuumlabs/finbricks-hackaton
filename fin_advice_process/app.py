import json
import os

import boto3 as boto3

TABLE_NAME = 'aiData'
REGION_NAME = 'eu-central-1'


def lambda_handler(event, context):
    query_parameters = event.get("queryStringParameters", {})
    client_id = query_parameters.get("clientId", "")
    print(event)
    lambda_inv = boto3.client("lambda", region_name="eu-central-1")
    response = lambda_inv.invoke(FunctionName=os.environ["AI_FUNCTION_ARN"],
                                 InvocationType='Event', Payload=json.dumps({"data": event["data"]}))
    response_payload = json.loads(response['Payload'].read())
    print(response_payload)

    dynamodb_config = {
        'region_name': REGION_NAME
    }
    dynamodb = boto3.resource('dynamodb', **dynamodb_config)
    table = dynamodb.Table(TABLE_NAME)


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_1_event.json")), None))

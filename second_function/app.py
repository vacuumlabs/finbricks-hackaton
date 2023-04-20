import json

import boto3 as boto3


def lambda_handler(event, context):
    print(event)
    return {
        "statusCode": 200,
        "body": "Hi, I'm Elfo!"
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("events/event.json")), None))
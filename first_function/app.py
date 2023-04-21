import json
import os

import boto3 as boto3


def lambda_handler(event, context):
    print(event)
    lambda_inv = boto3.client("lambda", region_name="eu-central-1")
    response = lambda_inv.invoke(FunctionName=os.environ["SECOND_FUNCTION_ARN"],  # 'finbricks-hackaton-SecondFunction-FqBGHnJ1bSCa',
                                 InvocationType='RequestResponse', Payload=json.dumps(event))
    response_payload = json.loads(response['Payload'].read())

    print(response_payload)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "FirstLamda says": "I'm working!",
            "SecondLambda says": response_payload["body"]
        })
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_1_event.json")), None))

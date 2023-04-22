import json
import os

import boto3 as boto3
import jwt
import requests

from first_function.aws import get_secret


def get_signature(endpoint, body, kid, private_key):
    jws_header = {"typ": "JWT", "alg": "RS256", "kid": kid}
    payload = {
        "uri": endpoint,
        "body": body}

    # print(payload)
    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256", headers=jws_header)
    split = encoded_jwt.split('.')
    return f'{split[0]}..{split[2]}'


def lambda_handler(event, context):
    private_key = json.loads(get_secret("finbricks_pk"))['value']

    kid = "ec9e2133-520f-4ca0-9e12-f167339d232e"
    client_id = "hackathon2023_vl"
    base_url = 'https://api.sandbox.finbricks.com'
    bank_account_id = 10037188
    transactions_endpoint = f'/account/transactions?merchantId={kid}&clientId={client_id}&paymentProvider=MOCK_COBS&bankAccountId={bank_account_id}'

    transactions_response = requests.get(
        f'{base_url}{transactions_endpoint}',
        headers={'JWS-Signature': get_signature(transactions_endpoint, "", kid, private_key)})

    result = ""

    if transactions_response.status_code == 200:
        for transaction in transactions_response.json()["transactions"]:
            target_creditor = transaction["entryDetails"]["transactionDetails"]["relatedParties"]["creditor"]
            creditor = target_creditor["name"] if target_creditor else \
                transaction["entryDetails"]["transactionDetails"]["relatedParties"]["creditorAccount"][
                    "identification"][
                    "other"]["identification"]
            result += f'{transaction["creditDebitIndicator"]} {transaction["valueDate"]["date"]} {transaction["amount"]["value"]} {transaction["amount"]["currency"]} {creditor} \n'

    print(result)

    lambda_inv = boto3.client("lambda", region_name="eu-central-1")
    response = lambda_inv.invoke(FunctionName=os.environ["SECOND_FUNCTION_ARN"],
                                 InvocationType='RequestResponse', Payload=json.dumps({"data": result}))
    response_payload = json.loads(response['Payload'].read())

    print(response_payload)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "results": [{"result": response_payload["body"]}],
        })
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_1_event.json")), None))

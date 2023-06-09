import json
import os

import boto3 as boto3
import jwt
import requests

from aws import get_secret


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
    query_parameters = event.get("queryStringParameters", {})
    client_id = query_parameters.get("clientId", "")

    private_key = get_secret("finbricks_pk4")

    kid = "ec9e2133-520f-4ca0-9e12-f167339d232e"
    base_url = 'https://api.sandbox.finbricks.com'
    client_income = os.environ.get("CLIENT_INCOME", "48000 CZK")
    client_goal = os.environ.get("CLIENT_GOAL", "save 5000 CZK a month")
    payment_provider = os.environ.get("PAYMENT_PROVIDER", "MOCK_COBS")
    accounts_endpoint = f'/account/listWithBalance?merchantId={kid}&clientId={client_id}&paymentProvider={payment_provider}'

    accounts_response = requests.get(
        f'{base_url}{accounts_endpoint}',
        headers={'JWS-Signature': get_signature(accounts_endpoint, "", kid, private_key)})

    accounts = accounts_response.json()
    bank_account_id = accounts[0]["id"]
    account_balance = accounts[0]["balance"]
    account_currency = accounts[0]["currency"]

    # TODO: when the api starts to support filtering based on direction, limit the search to only debit transactions
    transactions_endpoint = f'/account/transactions?merchantId={kid}&clientId={client_id}&paymentProvider={payment_provider}&bankAccountId={bank_account_id}'
    transactions_response = requests.get(
        f'{base_url}{transactions_endpoint}',
        headers={'JWS-Signature': get_signature(transactions_endpoint, "", kid, private_key)})

    result = ""
    status = ""

    if transactions_response.status_code == 200:
        for transaction in transactions_response.json()["transactions"]:
            target_creditor = transaction["entryDetails"]["transactionDetails"]["relatedParties"]["creditor"]
            creditor = target_creditor["name"] if target_creditor else \
                transaction["entryDetails"]["transactionDetails"]["relatedParties"]["creditorAccount"][
                    "identification"][
                    "other"]["identification"]
            result += f'{transaction["creditDebitIndicator"]} {transaction["valueDate"]["date"]} {transaction["amount"]["value"]} {transaction["amount"]["currency"]} {creditor} \n'
            status = "success"
    else:
        status = "fail"
        print(f'{transactions_response.status_code}: {transactions_response.json()}')

    data = {
        "financial_history": result,
        "balance": f"{account_balance} {account_currency}",
        "goal": client_goal,
        "income": client_income
    }

    lambda_inv = boto3.client("lambda", region_name="eu-central-1")
    lambda_inv.invoke(FunctionName=os.environ["SECOND_FUNCTION_ARN"],
                      InvocationType='Event', Payload=json.dumps({"client_id": client_id, "data": data}))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": status,
        })
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_1_event.json")), None))

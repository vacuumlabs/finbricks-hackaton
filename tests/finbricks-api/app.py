import json
import jwt
import os
import requests

private_key = open(os.environ["PK_PATH"], "r").read()

kid = "ec9e2133-520f-4ca0-9e12-f167339d232e"
clientId = "hackathon2023_vl"
base_url = 'https://api.sandbox.finbricks.com'
accounts_endpoint = f'/account/list?merchantId={kid}&clientId={clientId}&paymentProvider=MOCK_COBS'
bankAccountId=10037188
transactions_endpoint = f'/account/transactions?merchantId={kid}&clientId={clientId}&paymentProvider=MOCK_COBS&bankAccountId={bankAccountId}'

auth_endpoint = '/auth/authenticate'
auth_body = {
    "merchantId": kid,
    "clientId": clientId,
    "provider": "MOCK_COBS",
    "scope": "AISP",
    "callbackUrl": "https://mujweb.cz/redirect-from-fbx.html"
}


def get_signature(endpoint, body):
    jws_header = {"typ": "JWT", "alg": "RS256", "kid": kid}
    payload = {
        "uri": endpoint,
        "body": body}

    # print(payload)
    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256", headers=jws_header)
    split = encoded_jwt.split('.')
    return f'{split[0]}..{split[2]}'


auth_response = requests.post(
    f'{base_url}{auth_endpoint}',
    json=auth_body,
    headers={'JWS-Signature': get_signature(auth_endpoint, json.dumps(auth_body))}
)

accounts_response = requests.get(
    f'{base_url}{accounts_endpoint}',
    headers={'JWS-Signature': get_signature(accounts_endpoint, "")})

transactions_response = requests.get(
    f'{base_url}{transactions_endpoint}',
    headers={'JWS-Signature': get_signature(transactions_endpoint, "")})

if transactions_response.status_code == 200:
    for transaction in transactions_response.json()["transactions"]:
        target_creditor = transaction["entryDetails"]["transactionDetails"]["relatedParties"]["creditor"]
        creditor = target_creditor["name"] if target_creditor else transaction["entryDetails"]["transactionDetails"]["relatedParties"]["creditorAccount"]["identification"]["other"]["identification"]
        print(f'{transaction["creditDebitIndicator"]} {transaction["valueDate"]["date"]} {transaction["amount"]["value"]} {transaction["amount"]["currency"]} {creditor}')
else:
    print('Transaction fetch failed!')


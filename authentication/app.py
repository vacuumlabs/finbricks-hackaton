import json

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

    auth_endpoint = '/auth/authenticate'
    auth_body = {
        "merchantId": kid,
        "clientId": client_id,
        "provider": "MOCK_COBS",
        "scope": "AISP",
        "callbackUrl": "https://mujweb.cz/redirect-from-fbx.html"
    }

    auth_response = requests.post(
        f'{base_url}{auth_endpoint}',
        json=auth_body,
        headers={'JWS-Signature': get_signature(auth_endpoint, json.dumps(auth_body), kid, private_key)}
    )

    print(auth_response)

    auth_status = auth_response.json().get("authStatus", "")
    redirect_url = auth_response.json().get("redirectUrl", "")
    operation_id = auth_response.json().get("operationId", "")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "auth_status": auth_status,
            "redirect_url": redirect_url,
            "operation_id": operation_id
        })
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_1_event.json")), None))

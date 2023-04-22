import base64
from base64 import urlsafe_b64encode

import jwt
import requests
# from jose import jws

private_key = open("/Users/michalzan/.ssh/finbricks_private.pem", "r").read()

jwsHeader = '{"typ":"JWT", "alg":"RS256", "kid":"cb7f0803-143b-4f10-8cac-0657fa17b109"}'
encodedHeader = urlsafe_b64encode(jwsHeader.encode('utf-8')).decode('utf-8')

payload = {"uri":"/account/list?merchantId=ec9e2133-520f-4ca0-9e12-f167339d232e&clientId=hackathon2023_vl&paymentProvider=MOCK_COBS","body":""}

encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid":"cb7f0803-143b-4f10-8cac-0657fa17b109"})

jwsSignature = f"{encodedHeader}..{encoded_jwt}"

response = requests.get("https://api.sandbox.finbricks.com/account/list?merchantId=ec9e2133-520f-4ca0-9e12-f167339d232e&clientId=hackathon2023_vl&paymentProvider=MOCK_COBS", headers={'JWT-Signature': encoded_jwt})

print(jwsSignature)
print(response.json())

import json

import jwt, requests
from base64 import urlsafe_b64encode

private_key = open("/home/bohuss/projects/finbricks/finbricks_private.pem", "r").read()

b_private_key = b"${private_key}"


#{"uri":"/account/list?merchantId=ec9e2133-520f-4ca0-9e12-f167339d232e","body":""}

jwsHeader = b'{"typ":"JWT", "alg":"RS256", "kid":"cb7f0803-143b-4f10-8cac-0657fa17b109"}'

authBody = {
    "merchantId": "ec9e2133-520f-4ca0-9e12-f167339d232e",
    "clientId": "hackathon2023_vl",
    "provider": "MOCK_COBS",
    "scope": "AISP",
    "callbackUrl": "https://www.vacuumlabs.cz/callback"
}

payload = {"uri":"/account/list?merchantId=ec9e2133-520f-4ca0-9e12-f167339d232e&clientId=hackathon2023_vl&paymentProvider=MOCK_COBS","body":""}

encodedHeader = urlsafe_b64encode(jwsHeader)
# encodedPayload = urlsafe_b64encode(payload)
#
# data = f"${encodedHeader}.${encodedPayload}"

encoded_jwt = jwt.encode(payload, b_private_key, algorithm="HS256")

jwsSignature = f"${encodedHeader}..${encoded_jwt}"

response = requests.get("https://api.sandbox.finbricks.com/account/list?merchantId=ec9e2133-520f-4ca0-9e12-f167339d232e&clientId=hackathon2023_vl&paymentProvider=MOCK_COBS", headers={'JWS-Signature': jwsSignature})

print(response.json())

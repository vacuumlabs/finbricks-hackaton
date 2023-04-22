from base64 import urlsafe_b64encode

import jwt
import requests

private_key = open("/Users/michalzan/.ssh/finbricks_private.pem", "r").read()

b_private_key = b"${private_key}"


#{"uri":"/account/list?merchantId=ec9e2133-520f-4ca0-9e12-f167339d232e","body":""}

jwsHeader = b'{"typ":"JWT", "alg":"RS256", "kid":"cb7f0803-143b-4f10-8cac-0657fa17b109"}'

payload = {"uri":"/account/list?merchantId=ec9e2133-520f-4ca0-9e12-f167339d232e&clientId=hackathon2023_vl&paymentProvider=MOCK_COBS","body":""}

encodedHeader = urlsafe_b64encode(jwsHeader)
# encodedPayload = urlsafe_b64encode(payload)
#
# data = f"${encodedHeader}.${encodedPayload}"

encoded_jwt = jwt.encode(payload, b_private_key, algorithm="HS256", headers={"typ":"JWT", "alg":"HS256", "kid":"cb7f0803-143b-4f10-8cac-0657fa17b109"})
# encoded_Header = jwt.encode(jwsHeader)

jwsSignature = f"{encodedHeader}..{encoded_jwt}"

response = requests.get("https://api.sandbox.finbricks.com/account/list?merchantId=ec9e2133-520f-4ca0-9e12-f167339d232e&clientId=hackathon2023_vl&paymentProvider=MOCK_COBS", headers={'JWS-Signature': encoded_jwt})
print(jwsSignature)
print(response.json())

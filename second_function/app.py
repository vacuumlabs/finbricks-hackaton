import json
import os

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

from aws import get_secret

TEMPLATE = """
You act as a financial advisor called to the client of Vacuumlabs bank. You are very friendly, pleasant and fun.

You are very knowledgeable and knows what are the people weaknesses while managing their finances.

This is list of the monthly transactions with amounts, categories and subcategories:

TRANSFER	05/03/2023	500.0	From 8515877581@axisb	INCOME	OTHER
TRANSFER	08/03/2023	100.0	From 8515877581@axisb	INCOME	OTHER
CHARGE	08/03/2023	-100.0	PAYTM WALLET NOIDA IN	SERVICES	OTHER_SERVICES
TRANSFER	08/03/2023	1000.0	From 8515877581@axisb	INCOME	OTHER
CHARGE	08/03/2023	-1000.0	PAYTM WALLET NOIDA IN	SERVICES	OTHER_SERVICES
TRANSFER	08/03/2023	3000.0	From 8515877581@axisb	INCOME	OTHER
CHARGE	08/03/2023	-3000.0	PAYTM WALLET NOIDA IN	SERVICES	OTHER_SERVICES
CHARGE	07/03/2023	-500.0	Paytm_PaytmAddMoney 1204770770 IN	SERVICES	OTHER_SERVICES
TRANSFER	10/03/2023	410.0	From 8515877581@axisb	INCOME	OTHER
CHARGE	10/03/2023	-410.0	PAYTM PAYMENTS SERVICE NOIDA IN	TRANSPORT	REPAIRS_AND_MAINTENANCE

The monthly saving goal of 1000 Kc (CZK) was not met.

First, make concise, short paragraph summary of the transactions.

Then provide user some meaningful advice based specifically on the transaction summary paragraph and point out expense that can be most easily managed or ommited next month. Use direct language, speaking directly to the user.

Don't advise to pick up another job or reaching back to you.
{input}
"""


def get_chain():
    openai_api_key = json.loads(get_secret("OpenaiApiKey"))['OpenaiApiKey']

    llm = ChatOpenAI(temperature=0.8, max_retries=1, request_timeout=90, max_tokens=512, openai_api_key=openai_api_key)  # 30sec timeout, 0 retries for bot
    prompt = PromptTemplate(
        template=TEMPLATE,
        input_variables=["input"]
    )
    return LLMChain(llm=llm, prompt=prompt, output_key="result")


def lambda_handler(event, context):
    print(event)

    inputs = {
        "input": " "
    }

    llm_chain = get_chain()
    llm_results = llm_chain(inputs)
    print(llm_results)

    return {
        "statusCode": 200,
        "body": llm_results["result"]
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_2_event.json")), None))

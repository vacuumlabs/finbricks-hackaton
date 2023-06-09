import json

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

from aws import get_secret

# TODO load previous transactions from DB
TEMPLATE = """
Classify the following financial transaction data point with either ESSENTIAL or NON_ESSENTIAL:
=========
Transaction: DEBIT	17.04.2023	1279	CZK	MCDONALDS JINDRICHUV HRADEC
Category: NON_ESSENTIAL
Transaction: DEBIT	21.04.2023	3598	CZK	Spol.vl.jed.domu Vodova 92
Category: ESSENTIAL
Transaction: DEBIT	11.04.2023	1142	CZK	Platební brána ČSOB
Category: ESSENTIAL
Transaction: DEBIT	17.04.2023	3230	CZK	ESSENTIAL	EYELLO CZ, K.S.
Category: ESSENTIAL
=========

Transaction: {input}
Category:
"""


def get_chain():
    openai_api_key = json.loads(get_secret("OpenaiApiKey"))['OpenaiApiKey']

    llm = ChatOpenAI(temperature=0.0, max_retries=1, request_timeout=90, openai_api_key=openai_api_key)  # 30sec timeout, 0 retries for bot

    prompt = PromptTemplate(
        template=TEMPLATE,
        input_variables=["input"]
    )

    return LLMChain(llm=llm, prompt=prompt, output_key="result")


def lambda_handler(event, context):
    print(event)

    if "body" in event and event["body"] is not None and event["body"] != "null":
        inputs = event["body"]
    else:
        inputs = {"input": "DEBIT	06.04.2023	549	CZK	MCDONALDS JINDRICHUV HRADEC"}

    llm_chain = get_chain()
    llm_results = llm_chain(inputs)
    print(llm_results["result"])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "transaction": inputs,
            "result": llm_results["result"],
        })
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_2_event.json")), None))

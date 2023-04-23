import json
from pathlib import Path

from langchain import PromptTemplate, LLMChain
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI

from aws import get_secret

# TEMPLATE = """
# You act as a financial advisor called to the client of Vacuumlabs bank. You are very friendly, pleasant and fun.
#
# You are very knowledgeable and knows what are the people weaknesses while managing their finances.
#
# This is list of the monthly transactions with amounts, categories and subcategories:
#
# INCOME	05/03/2023	500.0	From 8515877581@axisb	INCOME	OTHER
# INCOME	08/03/2023	100.0	From 8515877581@axisb	INCOME	OTHER
# EXPENSE	08/03/2023	-100.0	PAYTM WALLET NOIDA IN	SERVICES	OTHER_SERVICES
# INCOME	08/03/2023	1000.0	From 8515877581@axisb	INCOME	OTHER
# EXPENSE	08/03/2023	-1000.0	PAYTM WALLET NOIDA IN	SERVICES	OTHER_SERVICES
# INCOME	08/03/2023	3000.0	From 8515877581@axisb	INCOME	OTHER
# EXPENSE	08/03/2023	-3000.0	PAYTM WALLET NOIDA IN	SERVICES	OTHER_SERVICES
# EXPENSE	07/03/2023	-500.0	Paytm_PaytmAddMoney 1204770770 IN	SERVICES	OTHER_SERVICES
# INCOME	10/03/2023	410.0	From 8515877581@axisb	INCOME	OTHER
# EXPENSE	10/03/2023	-410.0	PAYTM PAYMENTS SERVICE NOIDA IN	TRANSPORT	REPAIRS_AND_MAINTENANCE
#
# The monthly saving goal of 1000 Kc (CZK) was not met.
#
# First, make concise, short paragraph summary of the transactions.
#
# Then provide user some meaningful advice based specifically on the transaction summary paragraph and point out expense that can be most easily managed or ommited next month. Use direct language, speaking directly to the user.
#
# Don't advise to pick up another job or reaching back to you.
# {input}
# """

TEMPLATE_FINAL = """
You are a financial advisor of user Matej. His financial goal is to {goal}. The balance at the start of last month is {balance}. You are very friendly, pleasant and funny.

This is list of the transactions with dates, amounts, currencies and notes:

{financial_history}

Use direct language, speak directly to the user.
Don't advise to pick up another job or reaching back to you.

Use this structure:
==========
2 Sentences, maximum 300 characters: concise, short paragraph summary of the transactions
2 Sentences, maximum 300 characters: If the user can hit his financial goal {goal} without adjustments to his behavior provided his balance is {balance}, compliment him/her and suggest a reward with our sponsor: {sponsor}. If the user cannot hit his financial goal {goal} provided his balance is {balance}, provide a suggestion to hit the goal.
==========
"""
# Then provide user some meaningful advice based specifically on the transaction summary paragraph and point out expense that can be most easily managed or ommited next month and provide the amount.

TEMPLATE_SPONSORS_ = """
Given the following customer's financial transactions history and our sponsors, pick the sponsor that may interest our customer:

financial transactions history:
==========
{financial_history}
==========

sponsors:
==========
""" + Path('sponsors_ok').read_text() + """
==========

Provide a condensed message.
"""

def get_chain():
    openai_api_key = json.loads(get_secret("OpenaiApiKey"))['OpenaiApiKey']

    llm = ChatOpenAI(temperature=0.0, max_retries=1, request_timeout=90, max_tokens=1024, openai_api_key=openai_api_key)  # 30sec timeout, 0 retries for bot

    sponsors_prompt = PromptTemplate(
        template=TEMPLATE_SPONSORS_,
        input_variables=["financial_history"]
    )

    final_prompt = PromptTemplate(
        template=TEMPLATE_FINAL,
        input_variables=["balance", "financial_history", "sponsor", "goal"]
    )

    sponsors_chain = LLMChain(llm=llm, prompt=sponsors_prompt, output_key="sponsor")

    final_chain = LLMChain(llm=llm, prompt=final_prompt, output_key="result")

    return SequentialChain(
        chains=[sponsors_chain, final_chain],
        input_variables=["balance", "financial_history", "goal"],
        output_variables=["result"],
    )


def lambda_handler(event, context):
    print(event)

    inputs = [{
        "balance": "500000 CZK",
        "goal": "save 1000000 CZK for a new car until the end of this year",
        "financial_history": """
type	date	amount	currency		note
					
APRIL					
DEBIT	21.04.2023	2000	CZK	ESSENTIAL	ČEZ PRODEJ, A.S.
DEBIT	21.04.2023	3598	CZK	ESSENTIAL	Spol.vl.jed.domu Vodova 92
DEBIT	20.04.2023	1279	CZK	NON_ESSENTIAL	MCDONALDS JINDRICHUV HRADEC
CREDIT	20.04.2023	75000	CZK	INCOME	MGR. MATEJ PRISTAK
DEBIT	20.04.2023	31281	CZK	NON_ESSENTIAL	PRISTAK MATEJ
DEBIT	17.04.2023	1279	CZK	NON_ESSENTIAL	MCDONALDS JINDRICHUV HRADEC
DEBIT	17.04.2023	548	CZK	ESSENTIAL	O2 Czech Republic a.
DEBIT	17.04.2023	250	CZK	ESSENTIAL	STARNET, s.r.o.
DEBIT	17.04.2023	3230	CZK	ESSENTIAL	EYELLO CZ, K.S.
DEBIT	17.04.2023	1630	CZK	ESSENTIAL	EYELLO CZ, K.S.
DEBIT	15.04.2023	1279	CZK	NON_ESSENTIAL	MCDONALDS JINDRICHUV HRADEC
CREDIT	12.04.2023	20831	CZK	INCOME	UlovDomov.cz s.r.o.
DEBIT	11.04.2023	3830	CZK	ESSENTIAL	Spol.vl.jed.domu Vodova 92
DEBIT	11.04.2023	1142	CZK	ESSENTIAL	Platební brána ČSOB
DEBIT	06.04.2023	1279	CZK	NON_ESSENTIAL	MCDONALDS JINDRICHUV HRADEC
CREDIT	06.04.2023	802	CZK	INCOME	ZASILKOVNA S.R.O.
        """
    },
    {
            "balance": "500000 CZK",
            "goal": "save 1000000 CZK for a new car until the end of this year",
            "financial_history": """
    type	date	amount	currency		note

    APRIL					
    DEBIT	21.04.2023	2000	CZK	ESSENTIAL	ČEZ PRODEJ, A.S.
    DEBIT	21.04.2023	3598	CZK	ESSENTIAL	Spol.vl.jed.domu Vodova 92
    DEBIT	20.04.2023	1279	CZK	NON_ESSENTIAL	MCDONALDS JINDRICHUV HRADEC
    CREDIT	20.04.2023	175000	CZK	INCOME	MGR. MATEJ PRISTAK
    DEBIT	20.04.2023	31281	CZK	NON_ESSENTIAL	PRISTAK MATEJ
    DEBIT	17.04.2023	1279	CZK	NON_ESSENTIAL	MCDONALDS JINDRICHUV HRADEC
    DEBIT	17.04.2023	548	CZK	ESSENTIAL	O2 Czech Republic a.
    DEBIT	17.04.2023	250	CZK	ESSENTIAL	STARNET, s.r.o.
    DEBIT	17.04.2023	3230	CZK	ESSENTIAL	EYELLO CZ, K.S.
    DEBIT	17.04.2023	1630	CZK	ESSENTIAL	EYELLO CZ, K.S.
    DEBIT	15.04.2023	1279	CZK	NON_ESSENTIAL	MCDONALDS JINDRICHUV HRADEC
    CREDIT	12.04.2023	20831	CZK	INCOME	UlovDomov.cz s.r.o.
    DEBIT	11.04.2023	3830	CZK	ESSENTIAL	Spol.vl.jed.domu Vodova 92
    DEBIT	11.04.2023	1142	CZK	ESSENTIAL	Platební brána ČSOB
    DEBIT	06.04.2023	1279	CZK	NON_ESSENTIAL	MCDONALDS JINDRICHUV HRADEC
    CREDIT	06.04.2023	802	CZK	INCOME	ZASILKOVNA S.R.O.
            """
    }
]

    llm_chain = get_chain()
    llm_results = llm_chain(inputs[1])
    print(llm_results["result"])

    return {
        "statusCode": 200,
        "body": {
            "result": llm_results["result"],
        }
    }


# Test locally
if __name__ == "__main__":
    print(lambda_handler(json.load(open("../events/function_2_event.json")), None))

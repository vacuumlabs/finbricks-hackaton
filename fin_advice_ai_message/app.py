import json
from pathlib import Path

from langchain import PromptTemplate, LLMChain
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI

from aws import get_secret

TEMPLATE_FINAL = """
You are a financial advisor of user Matej. His financial goal is to {goal}. His balance at the start of last month was {balance}. His monthly income is {income}.

This is list of the transactions with dates, amounts, currencies and notes:
==================
{financial_history}
==================

You are very friendly, pleasant and funny.
Use direct language, speak directly to the user.

Use this structure:
==========
2 Sentences, maximum 300 characters: Concise, short paragraph summary of the spending overview
empty line
2 Sentences, maximum 300 characters: Short summary of the status of user's financial goal {goal}. Compliment him/her.
empty line
2 Sentences, maximum 300 characters: Provide user some meaningful advice based specifically on the transaction summary paragraph and point out expense that can be most easily managed or ommited next month and provide the amount. Don't advise to pick up another job or reaching back to you. 
==========
"""

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

    llm = ChatOpenAI(temperature=0.8, max_retries=1, request_timeout=90, max_tokens=1024, openai_api_key=openai_api_key, model="gpt-4")  # 30sec timeout, 0 retries for bot

    final_prompt = PromptTemplate(
        template=TEMPLATE_FINAL,
        input_variables=["balance", "financial_history", "goal", "income"]
    )

    return LLMChain(llm=llm, prompt=final_prompt, output_key="result")

    ### uncomment to add sponsor messages
    # sponsors_prompt = PromptTemplate(
    #     template=TEMPLATE_SPONSORS_,
    #     input_variables=["financial_history"]
    # )
    # sponsors_chain = LLMChain(llm=llm, prompt=sponsors_prompt, output_key="sponsor")
    # return SequentialChain(
    #     chains=[sponsors_chain, final_chain],
    #     input_variables=["balance", "financial_history", "goal", "income"],
    #     output_variables=["result"],
    # )


def lambda_handler(event, context):
    print(event)

    llm_chain = get_chain()
    llm_results = llm_chain(event)
    print(llm_results["result"])

    return {
        "statusCode": 200,
        "body": {
            "result": llm_results["result"],
        }
    }


# Test locally
if __name__ == "__main__":
    inputs = {
        #         "balance": "1000 CZK",
        #         "goal": "save 1000000 CZK for a new house",
        #         "financial_history": """
        # type|date|amount|currency|note
        # DEBIT|21.04.2023|2000|CZK|ESSENTIAL|ČEZ PRODEJ, A.S.
        # DEBIT|21.04.2023|3598|CZK|ESSENTIAL|Spol.vl.jed.domu Vodova 92
        # DEBIT|20.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        # CREDIT|20.04.2023|55000|CZK|INCOME|MGR. MATEJ PRISTAK
        # DEBIT|20.04.2023|31281|CZK|NON_ESSENTIAL|PRISTAK MATEJ
        # DEBIT|17.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        # DEBIT|17.04.2023|548|CZK|ESSENTIAL|O2 Czech Republic a.
        # DEBIT|17.04.2023|250|CZK|ESSENTIAL|STARNET, s.r.o.
        # DEBIT|17.04.2023|3230|CZK|ESSENTIAL|EYELLO CZ, K.S.
        # DEBIT|17.04.2023|1630|CZK|ESSENTIAL|EYELLO CZ, K.S.
        # DEBIT|15.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        # CREDIT|12.04.2023|20831|CZK|INCOME|UlovDomov.cz s.r.o.
        # DEBIT|11.04.2023|3830|CZK|ESSENTIAL|Spol.vl.jed.domu Vodova 92
        # DEBIT|11.04.2023|1142|CZK|ESSENTIAL|Platební brána ČSOB
        # DEBIT|06.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        # CREDIT|06.04.2023|802|CZK|INCOME|ZASILKOVNA S.R.O.
        # """
        # In April, you had a total income of 78,633 CZK and spent 45,736 CZK, with essential expenses being 27,277 CZK and non-essential expenses totaling 18,459 CZK.
        #
        # With your current savings rate, you are moving closer to your goal of saving 1,000,000 CZK for a new house. Great job! As a reward, you might enjoy our sponsor's offer, "Degustační menu na Pivolodi."
        #
        # To improve your savings, consider reducing non-essential expenses, such as the 5,116 CZK spent on McDonald's visits. Cutting back on these outings could significantly increase your monthly savings.

        #             "balance": "500000 CZK",
        #             "goal": "save 1000000 CZK for a new car until the end of this year",
        #             "financial_history": """
        #     type|date|amount|currency|note
        #     DEBIT|21.04.2023|2000|CZK|ESSENTIAL|ČEZ PRODEJ, A.S.
        #     DEBIT|21.04.2023|3598|CZK|ESSENTIAL|Spol.vl.jed.domu Vodova 92
        #     DEBIT|20.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        #     CREDIT|20.04.2023|275000|CZK|INCOME|MGR. MATEJ PRISTAK
        #     DEBIT|20.04.2023|11281|CZK|NON_ESSENTIAL|PRISTAK MATEJ
        #     DEBIT|17.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        #     DEBIT|17.04.2023|548|CZK|ESSENTIAL|O2 Czech Republic a.
        #     DEBIT|17.04.2023|250|CZK|ESSENTIAL|STARNET, s.r.o.
        #     DEBIT|17.04.2023|3230|CZK|ESSENTIAL|EYELLO CZ, K.S.
        #     DEBIT|17.04.2023|1630|CZK|ESSENTIAL|EYELLO CZ, K.S.
        #     DEBIT|15.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        #     CREDIT|12.04.2023|20831|CZK|INCOME|UlovDomov.cz s.r.o.
        #     DEBIT|11.04.2023|3830|CZK|ESSENTIAL|Spol.vl.jed.domu Vodova 92
        #     DEBIT|11.04.2023|1142|CZK|ESSENTIAL|Platební brána ČSOB
        #     DEBIT|06.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        #     CREDIT|06.04.2023|802|CZK|INCOME|ZASILKOVNA S.R.O.
        # """
        # Hey Matej, in April you had a total income of 304,633 CZK and spent 27,036 CZK, with 9,066 CZK on non-essential expenses like McDonald's visits.
        #
        # Great job on saving so far! You're halfway to your goal of 1,000,000 CZK for a new car by the end of the year. Treat yourself to a "Degustační menu na Pivolodi" for a unique dining experience with beer tasting.
        #
        # To save even more, consider cutting back on non-essential expenses like McDonald's visits, which totaled 5,116 CZK in April. Reducing these expenses could help you reach your goal even faster.

        "balance": "1000 CZK",
        "goal": "save 5000 CZK a month",
        "income": "48000 CZK",
        "financial_history": """
        type|date|amount|currency|note
        DEBIT|21.04.2023|2000|CZK|ESSENTIAL|ČEZ PRODEJ, A.S.
        DEBIT|21.04.2023|3598|CZK|ESSENTIAL|Spol.vl.jed.domu Vodova 92
        DEBIT|20.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        DEBIT|20.04.2023|31281|CZK|NON_ESSENTIAL|PRISTAK MATEJ
        DEBIT|17.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        DEBIT|17.04.2023|548|CZK|ESSENTIAL|O2 Czech Republic a.
        DEBIT|17.04.2023|250|CZK|ESSENTIAL|STARNET, s.r.o.
        DEBIT|17.04.2023|3230|CZK|ESSENTIAL|EYELLO CZ, K.S.
        DEBIT|17.04.2023|1630|CZK|ESSENTIAL|EYELLO CZ, K.S.
        DEBIT|15.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        DEBIT|11.04.2023|3830|CZK|ESSENTIAL|Spol.vl.jed.domu Vodova 92
        DEBIT|11.04.2023|1142|CZK|ESSENTIAL|Platební brána ČSOB
        DEBIT|06.04.2023|1279|CZK|NON_ESSENTIAL|MCDONALDS JINDRICHUV HRADEC
        """
        # Hey Matej, you rockin' spender! Last month you had a total outgoing of 45,826 CZK, with 23,579 CZK on essential expenses and 22,247 CZK on non-essential ones.
        #
        # Amazingly, your balance ended at 4,174 CZK, which means you almost reached your goal to save 5,000 CZK a month. High five!
        #
        # Now, let's make a tiny change to hit that goal: maybe cut down on those tasty McDonald's trips, which cost you 5,116 CZK last month. With this tweak, you'll be a saving superstar in no time!
    }

    print(lambda_handler(inputs, None))

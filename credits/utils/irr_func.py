import locale as lc

import numpy_financial as npf

def get_irr(initial_investment, cash_flows):
    params = create_params(initial_investment, cash_flows)
    return calculate_irr(params)

def create_params(initial_investment, cash_flows):
    params = []
    if initial_investment > 0:
        initial_investment = -1 * initial_investment
    params.append(initial_investment)
    params.extend(cash_flows)
    return params

"""
    Calculate the internal rate of return of a series of cash flows.
    Sample: round(npf.irr([-100, 39, 59, 55, 20]), 5)
"""
def calculate_irr(param):
    return round(npf.irr(param), 5)


def calculate_interest(current_amount, irr, tax_bsmv, tax_kkdf):
    return irr * (current_amount / (1 + get_tax_by_credit_type(tax_bsmv, tax_kkdf)))

def calculate_tax(interest, tax_bsmv, tax_kkdf):
    return interest * get_tax_by_credit_type(tax_bsmv, tax_kkdf)

def calculate_prn(credit, interest, tax):
    return credit - interest - tax

def calculate_rm_prn(current_amount, principal_amount):
    return current_amount - principal_amount

def get_tax_by_credit_type(tax_bsmv, tax_kkdf):
    return tax_bsmv + tax_kkdf

"""
    1 Ticari
    2 Bireysel
"""
def get_credit_type(credit_type):
    if credit_type == 1:
        return 1
    elif credit_type == 2:
        return 2
    else:
        return 0

"""
    1 İhtiyac
    2 Konut
    3 Taşıt
"""
def get_consumer_credit_type(consumer_credit_type):
    if consumer_credit_type == 1:
        return 1
    elif consumer_credit_type == 2:
        return 2
    elif consumer_credit_type == 3:
        return 3
    else:
        return 0

def calculate_interest_of_credit_blockage(block_amount, block_day, irr):
    x = pow((1 + irr), (block_day / 30))
    res = block_amount - (block_amount / x)
    return res

def transform(value):
    lc.setlocale(lc.LC_ALL, 'en_US.UTF-8') ## tr_TR.UTF-8
    rounded_value = round(value, 2)
    return lc.currency(rounded_value, symbol=False, grouping=True)

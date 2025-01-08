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


def calculate_interest(current_amount, irr):
    return irr * (current_amount / (1 + get_tax_by_credit_type()))

def calculate_tax(interest):
    return interest * get_tax_by_credit_type()

def calculate_prn(credit, interest, tax):
    return credit - interest - tax

def calculate_rm_prn(current_amount, principal_amount):
    return current_amount - principal_amount

def get_tax_by_credit_type():
    return 5
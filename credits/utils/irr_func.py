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

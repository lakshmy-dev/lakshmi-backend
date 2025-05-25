from typing import Dict, Any
from datetime import datetime

def goal_retirement(inputs: Dict[str, Any], tags: Dict[str, str]) -> Dict[str, Any]:
    """
    Retirement projection logic with real return (inflation-adjusted)

    inputs expected:
    {
        "current_age": 30,
        "retirement_age": 60,
        "current_savings": 200000,
        "monthly_savings": 10000,
        "expected_corpus": 10000000,
        "expected_return_rate": 0.10,    # optional override
        "inflation_rate": 0.06           # optional override
    }
    """

    # 🟡 Step 1: Base inputs and assumptions
    current_age = inputs.get("current_age", 30)
    retirement_age = inputs.get("retirement_age", 60)
    years_to_go = retirement_age - current_age

    current_savings = inputs.get("current_savings", 0)
    monthly_savings = inputs.get("monthly_savings", 10000)
    expected_corpus = inputs.get("expected_corpus", 10000000)

    # 🟡 Step 2: Return & Inflation assumptions
    risk_tag = tags.get("risk_appetite", "Moderate Risk-Taker")
    if risk_tag == "High Risk-Taker":
        annual_return = 0.12
    elif risk_tag == "Risk-Averse":
        annual_return = 0.06
    else:
        annual_return = 0.09

    annual_return = inputs.get("expected_return_rate", annual_return)
    inflation = inputs.get("inflation_rate", 0.06)

    monthly_return = (1 + annual_return) ** (1/12) - 1

    # 🟡 Step 3: Compound SIP projection
    future_value = current_savings
    projection = []

    for month in range(1, years_to_go * 12 + 1):
        future_value = future_value * (1 + monthly_return) + monthly_savings
        if month % 12 == 0:
            year = current_age + month // 12
            projection.append({
                "year": year,
                "age": year,
                "projected_value": round(future_value)
            })

    # 🟡 Step 4: Inflation-adjusted corpus
    present_value = expected_corpus / ((1 + inflation) ** years_to_go)
    real_future_value = future_value / ((1 + inflation) ** years_to_go)

    return {
        "final_value_nominal": round(future_value),
        "final_value_real": round(real_future_value),
        "target_corpus_nominal": expected_corpus,
        "target_corpus_real": round(present_value),
        "goal_met_nominal": future_value >= expected_corpus,
        "goal_met_real": real_future_value >= present_value,
        "surplus_or_gap_nominal": round(future_value - expected_corpus),
        "surplus_or_gap_real": round(real_future_value - present_value),
        "inflation_rate": inflation,
        "return_rate": annual_return,
        "projection": projection
    }

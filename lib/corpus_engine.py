import math
from typing import Dict, List, Any

def calculate_corpus(user_input: Dict[str, Any]) -> Dict[str, Any]:
    current_age = user_input.get("current_age", 30)
    retirement_age = user_input.get("retirement_age", 60)
    life_expectancy = user_input.get("life_expectancy", 85)
    monthly_contribution = user_input.get("monthly_contribution", 10000)

    expected_return = user_input.get("expected_return", 0.10)
    post_retirement_return = user_input.get("post_retirement_return", 0.06)
    inflation_rate = user_input.get("inflation_rate", 0.06)
    lifestyle_multiplier = user_input.get("lifestyle_multiplier", 1.0)

    # Optional extras
    windfall = user_input.get("windfallAmount", 0)
    major_expense = user_input.get("majorExpense", 0)
    gold_inheritance = user_input.get("goldOrInheritance", 0)
    emergency_buffer = user_input.get("emergencyBuffer", 0)
    epf_pct = user_input.get("epfContribution", 0)
    optimism_bias = user_input.get("optimismBias", 0)
    salary_growth_rate = user_input.get("salary_growth_rate", 0)

    goals = user_input.get("goals", [])
    income_streams = user_input.get("income_streams", [])
    current_year = user_input.get("current_year", 2025)
    start_year = current_year
    retirement_year = current_year + (retirement_age - current_age)
    end_year = current_year + (life_expectancy - current_age)
    years_to_retirement = retirement_age - current_age

    # Adjust goals
    adjusted_goal_corpus = 0
    for goal in goals:
        if goal.get("include", True):
            cost = goal.get("cost", 0)
            year = goal.get("year", retirement_year)
            years_to_goal = max(0, year - current_year)
            inflation_multiplier = math.pow(1 + inflation_rate, years_to_goal)
            adjusted_cost = cost * inflation_multiplier
            adjusted_goal_corpus += adjusted_cost

    # Expense assumption
    retirement_monthly_expense_pv = user_input.get("retirement_monthly_expense_pv")
    if not retirement_monthly_expense_pv:
        retirement_monthly_expense_pv = monthly_contribution * lifestyle_multiplier

    retirement_monthly_expense_fv = retirement_monthly_expense_pv * math.pow(1 + inflation_rate, years_to_retirement)
    retirement_duration_years = life_expectancy - retirement_age

    # Required corpus (FV)
    r = post_retirement_return
    annual_expense = retirement_monthly_expense_fv * 12
    corpus_required = (annual_expense * (1 - math.pow(1 + r, -retirement_duration_years))) / r

    total_required = corpus_required + adjusted_goal_corpus
    total_required_today = total_required / math.pow(1 + inflation_rate, years_to_retirement)

    # FV of contribution
    months_to_retirement = years_to_retirement * 12
    monthly_rate = expected_return / 12
    fv_base = monthly_contribution * (((math.pow(1 + monthly_rate, months_to_retirement) - 1) / monthly_rate) * (1 + monthly_rate))

    # Add EPF if any
    if epf_pct > 0:
        yearly_epf = epf_pct / 100 * (monthly_contribution * 12)
        fv_epf = 0
        for i in range(years_to_retirement):
            fv_epf = (fv_epf + yearly_epf) * (1 + expected_return)
        fv_base += fv_epf

    # Add/Subtract other items
    if windfall: fv_base += windfall
    if gold_inheritance: fv_base += gold_inheritance
    if major_expense: fv_base -= major_expense
    if emergency_buffer: fv_base -= emergency_buffer

    # Optimism bias
    if optimism_bias != 0:
        fv_base *= (1 + optimism_bias / 100)

    # Adjusted projection after goals
    adjusted_savings_after_goals = fv_base

    # Summary
    projection_summary = {
        "corpus_required": round(total_required, 0),
        "corpus_required_today": round(total_required_today, 0),
        "adjusted_goal_corpus": round(adjusted_goal_corpus, 0),
        "retirement_monthly_expense_pv": round(retirement_monthly_expense_pv, 0),
        "retirement_monthly_expense_fv": round(retirement_monthly_expense_fv, 0),
        "projected_savings": round(adjusted_savings_after_goals, 0),
        "corpus_gap": round(total_required - adjusted_savings_after_goals, 0),
        "on_track": adjusted_savings_after_goals >= total_required,
        "years_to_retirement": years_to_retirement,
        "years_in_retirement": retirement_duration_years
    }

    # Year-by-year balance simulation
    yearly_projection = []
    balance = 0
    for year in range(start_year, end_year + 1):
        if year < retirement_year:
            balance += monthly_contribution * 12
            balance *= (1 + expected_return)
        else:
            balance -= retirement_monthly_expense_fv * 12
            if balance < 0:
                balance = 0
            balance *= (1 + post_retirement_return)

        yearly_projection.append({
            "year": year,
            "balance": round(balance)
        })

    return {
        "summary": projection_summary,
        "yearly_projection": yearly_projection,
        "tags": [],
        "insights": []
    }

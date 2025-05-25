def format_currency_indian(amount: float) -> str:
    """
    Formats a numeric amount into Indian readable currency:
    - ₹1.83 Cr
    - ₹42.5 Lakh
    - ₹85,000
    """

    if amount >= 10_000_000:
        return f"₹{amount / 10_000_000:.2f} Cr"
    elif amount >= 100_000:
        return f"₹{amount / 100_000:.2f} Lakh"
    elif amount >= 1_000:
        return "₹{:,}".format(int(round(amount)))
    else:
        return f"₹{int(round(amount))}"

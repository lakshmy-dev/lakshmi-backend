from utils.format_utils import format_currency_indian


def build_lakshmi_summary(
    future_value: float,
    npv: float,
    gap_to_goal: float,
    tags: dict = None,
    scenario_type: str = "goal_retirement"
) -> str:
    """
    Builds a friendly, GPT-style summary from the projection results.
    Mimics Lakshmi’s tone of voice: kind, clear, smart, motivating.
    """

    fv_text = format_currency_indian(future_value)
    npv_text = format_currency_indian(npv)
    gap_text = format_currency_indian(abs(gap_to_goal))

    persona = tags.get("goal_orientation") or tags.get("emotional_money_behavior") if tags else ""

    tone_line = {
        "Short-Term Achiever": "You love ticking off goals fast ⚡",
        "Long-Term Builder": "You’re in it for the long haul ⏳",
        "Security-Seeker": "You like safety — let's make your future rock-solid 🛡️",
        "Instant Gratifier": "It’s okay to want results fast — we’ll get there 🎯"
    }.get(persona, "")

    if gap_to_goal >= 0:
        summary = (
            f"You’re on track! 💪 You’re projected to build a corpus of {fv_text}, "
            f"which is worth {npv_text} in today’s money.\n"
            f"{tone_line}"
        )
    else:
        summary = (
            f"You may fall short by {gap_text} if things continue like this. "
            f"Your projected corpus is {fv_text}, which is worth {npv_text} today.\n"
            f"But don’t worry — a few tweaks can change everything. 🚀\n"
            f"{tone_line}"
        )

    return summary.strip()

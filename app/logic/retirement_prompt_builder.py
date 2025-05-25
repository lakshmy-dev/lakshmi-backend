def build_retirement_prompt(
    projections: dict,
    tags: dict,
    user_name: str = "You"
) -> dict:
    """
    Returns Claude-ready prompt for GPT summary generation.

    Inputs:
    - projections: output from goal_retirement()
    - tags: semantic tags from user profile
    - user_name: optional personalization

    Output: Claude-compatible dict with system and user messages
    """

    # 1. Extract important metrics
    real_value = projections.get("final_value_real", 0)
    nominal_value = projections.get("final_value_nominal", 0)
    target_real = projections.get("target_corpus_real", 0)
    surplus_real = projections.get("surplus_or_gap_real", 0)
    goal_met = projections.get("goal_met_real", False)

    # 2. Tone & behavior tags
    tone = tags.get("tone_preference", "Straightforward")
    behavior = tags.get("savings_habit", "Regular Saver")
    orientation = tags.get("goal_orientation", "Long-Term Builder")

    # 3. Claude prompt (default Lakshmi vibe)
    system_prompt = f"""
You are Lakshmi, a smart and stylish financial coach for Indian users.
Your job is to summarize financial projections like a relatable mentor.
Tone: {tone}. Vibe: always cool, grounded, emotionally intelligent.
Never robotic. Be clear, not cringey. One-liners > paragraphs.
"""

    user_prompt = f"""
{user_name} is planning for retirement.

Here’s the projection summary:
- Final corpus: ₹{nominal_value:,}
- Real value today: ₹{real_value:,}
- Target (real terms): ₹{target_real:,}
- Surplus: ₹{surplus_real:,}
- Goal met: {"Yes ✅" if goal_met else "Not yet ❌"}

They are tagged as a "{behavior}" and "{orientation}".

Write a brief, 3–5 line summary in a coaching tone.
Make it feel like someone who “gets them.”
End with a suggestion or encouragement.
"""

    return {
        "system": system_prompt.strip(),
        "messages": [{"role": "user", "content": user_prompt.strip()}]
    }

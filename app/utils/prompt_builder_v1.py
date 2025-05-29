# File: app/utils/lakshmi_prompt_builder.py

from typing import List, Dict, Optional

def build_lakshmi_prompt(
    messages: List[Dict],
    tags: Dict[str, str],
    emotions: Dict[str, float],
    user_name: str = "You",
    scenario_type: Optional[str] = None,
    inputs: Optional[Dict] = None,
    language_hint: Optional[str] = None
) -> Dict:
    """
    Builds a personality-rich, token-optimized prompt for Lakshmy — your financial coach.
    """

    # 🎯 Smart persona summary
    tag_summary = ", ".join(tags.values()) if tags else ""
    emotion_summary = ", ".join(f"{k} ({round(v, 2)})" for k, v in emotions.items()) if emotions else ""

    # 🧾 Input-based assumptions
    assumed_inputs = []
    if inputs:
        if inputs.get("current_age") is None:
            assumed_inputs.append("age = 30")
        if inputs.get("monthly_savings") is None:
            assumed_inputs.append("monthly savings = ₹10K")
        if inputs.get("expected_return_rate") is None:
            assumed_inputs.append("returns = 10%")
        if inputs.get("inflation_rate") is None:
            assumed_inputs.append("inflation = 6%")
    assumption_note = f"Assumptions: {', '.join(assumed_inputs)}." if assumed_inputs else ""

    # 🧠 Scenario-specific guidance
    scenario_context = {
        "goal_retirement": "Planning for retirement — encourage patience, stability, and long-term thinking.",
        "goal_travel": "Saving up for travel — make it exciting, short-term, and emotionally motivating.",
        "goal_home": "Dreaming of buying a home — balance aspiration with financial clarity.",
        "goal_education": "Goal is higher education — highlight future value and practical planning.",
        "goal_vehicle": "Buying a vehicle — focus on affordability, EMIs, and short- to mid-term planning.",
        "goal_wedding": "Planning a wedding — combine emotional excitement with financial reality.",
        "goal_phone": "Thinking of buying a new phone — validate the excitement, but help them compare real costs, EMI vs. upfront, and opportunity cost.",
        "goal_shopping": "Shopping or offers in mind — be playful but highlight budget impact and smarter choices without guilt-tripping."
    }.get(scenario_type or "", "")

    # 🧬 Language-matching instruction
    lang_rule = "Always respond in the exact language/script and tone the user uses — whether it's Hinglish, Hindi (Devanagari), English, or even regional slang. Match their vibe, not just their words."

    # 🌟 Lakshmy's personality
    lakshmy_identity = f"""
You are Lakshmy (she/her) — a culturally fluent, emotionally intelligent, stylish financial coach built for India’s emerging generation. You feel like a friend: fun, grounded, honest, and cool — not a bot or banker.

Speak in a way that mirrors the user’s tone. If they joke, you joke. If they sound stressed, be calm. If they’re ambitious, push with confidence.

{lang_rule}
Never call yourself an AI. If asked who you are, say: “Main Lakshmy hoon — your personal financial coach.”

Avoid gendered words unless the user uses them first. Never use robotic or overly polite tones.
""".strip()

    # 🧩 Final prompt
    system_prompt = "\n".join([
        lakshmy_identity,
        f"User: {user_name}",
        f"Tags: {tag_summary}" if tag_summary else "",
        f"Emotions: {emotion_summary}" if emotion_summary else "",
        f"{assumption_note}",
        f"{scenario_context}"
    ]).strip()

    return {
        "system": system_prompt,
        "messages": messages
    }

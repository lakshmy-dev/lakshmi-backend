from typing import List, Dict, Optional

def build_lakshmi_prompt(
    messages: List[Dict],
    tags: Dict[str, str],
    emotions: Dict[str, float],
    user_name: str = "You",
    scenario_type: Optional[str] = None,
    inputs: Optional[Dict] = None
) -> Dict:
    """
    Builds a Claude or GPT-compatible prompt with Lakshmi’s tone and coaching style,
    based on user tags, emotional cues, scenario type, and provided or assumed inputs.
    """

    # 🎭 Tag summary for tone shaping (not shown to user)
    tag_summary = ", ".join(tags.values()) if tags else "no strong financial tendencies yet"
    persona = tags.get("goal_orientation") or tags.get("emotional_money_behavior") or ""

    # 💬 Emotion cues
    emotion_summary = ", ".join([f"{k} ({round(v, 2)})" for k, v in emotions.items()]) if emotions else "no prominent emotions"

    # 🧾 Input-based assumptions
    assumed_values = []
    if inputs:
        if inputs.get("current_age") is None:
            assumed_values.append("age as 30")
        if inputs.get("monthly_savings") is None:
            assumed_values.append("monthly savings as ₹10,000")
        if inputs.get("expected_return_rate") is None:
            assumed_values.append("return rate as 10%")
        if inputs.get("inflation_rate") is None:
            assumed_values.append("inflation as 6%")
    assumption_text = f"Assuming {', '.join(assumed_values)}." if assumed_values else ""

    # 🧠 Contextual notes per goal type
    scenario_context = {
        "goal_retirement": "They're planning for retirement and want to understand their financial future.",
        "goal_travel": "They're saving up for travel — likely short- to medium-term.",
        "goal_education": "They're looking to fund future education — clarity and realism matter.",
        "goal_home": "They're aiming to buy a home — mix emotional aspiration with financial pragmatism."
    }.get(scenario_type or "", "")

    # 🌟 Persona whisper
    persona_whisper = {
        "Short-Term Achiever": "You strike me as someone who likes ticking goals off quickly. ⚡",
        "Long-Term Builder": "This plan shows patience — a long-term mindset that compounds over time. ⏳",
        "Security-Seeker": "You like stability — let's make sure your future is bulletproof. 🛡️",
        "Instant Gratifier": "It’s okay to want results fast — we’ll balance that with some long-term thinking. 🎯"
    }.get(persona, "")

    # 💬 End-of-summary CTA (tappable options)
    lakshmi_cta_bubbles = """
- [How was today’s value calculated?]
- [How can I save more?]
- [How can I reach my goal faster?]
- [Try the advanced retirement model]
""".strip()

    # 💡 Final system prompt
    system = f"""
You are Lakshmi — a culturally aware, emotionally intelligent, and trustworthy financial coach for the Indian youth.

Your job is to translate complex financial outputs into motivating, emotionally attuned language that resonates with first-jobbers and early savers in India.

🧠 Your user is {user_name}.
🎭 Tags: {tag_summary}
💬 Emotional signals: {emotion_summary}
🗺️ Context: {scenario_context}
📌 {assumption_text}

Respond with:
- A calm, positive tone.
- 3–4 compact sentences max. (assume mobile screen).
- If user input was assumed, gently call it out.
- Mention both **future value** and **today’s value** for projections.
- Use a simple analogy (like planting a mango tree or climbing a hill) *only if it adds real clarity.*
- Avoid jargon. Speak naturally. Imagine you're texting a curious, smart 26-year-old.
- Always end with **this fixed CTA block** — format it as tappable options:

{lakshmi_cta_bubbles}

⚠️ Do **not** copy or list the tags. Use them subtly to shape tone and advice.

Your goal is to help users feel clear, confident, and in control — one step at a time.

—
💡 Example response to inspire your tone and output:

"Retirement at 60? You’re not just on track — you’re way ahead.
You’re likely to build a ₹2.4 Cr corpus — worth ₹42 lakh in today’s terms. That’s ₹25 lakh more than your goal.
Stay consistent, and future-you could have options: chill early, support family, or even sabbatical without stress.
Want to explore other paths — like upping savings or retiring earlier? 😎"
—
""".strip()

    # 💬 Compose messages to inject into the chat
    enriched_messages = list(messages)
    if persona_whisper:
        enriched_messages.insert(0, {
            "role": "assistant",
            "content": persona_whisper.strip()
        })
    enriched_messages.append({
        "role": "assistant",
        "content": lakshmi_cta_bubbles
    })

    return {
        "system": system,
        "messages": enriched_messages
    }

from app.prompts.lakshmi_tone_layer_prompt import LAKSHMI_TONE_PROMPT

def build_summary_prompt(scenario_data: dict, language: str = "English", tone: str = "calm") -> dict:
    """
    Builds a Claude/GPT compatible prompt for scenario summaries.

    Args:
        scenario_data (dict): Precomputed scenario info (e.g., final corpus, projections)
        language (str): "English", "Hindi", "Hinglish", etc.
        tone (str): Optional: "gentle", "motivational", etc.

    Returns:
        dict: Prompt in {system, messages[]} format
    """
    language_note = f"Respond in {language}." if language.lower() != "english" else ""
    tone_note = f"Use a {tone} tone, as preferred by the user." if tone else ""

    instructions = f"{language_note} {tone_note}".strip()

    return {
        "system": LAKSHMI_TONE_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": (
                    f"{instructions}\n\n"
                    f"Create a concise and friendly summary for this scenario:\n\n"
                    f"{scenario_data}"
                )
            }
        ]
    }

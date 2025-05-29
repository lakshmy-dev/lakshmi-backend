# File: middle_layer/tag_engine.py

import re

# -- Master Tag Rules: Covers all 9 categories
TAG_RULES = {
    "income_status": {
        "No Income": ["student", "no job", "unemployed", "searching for job"],
        "Freelancing": ["freelance", "project-based", "contract work"],
        "Salaried-Fixed": ["salary", "fixed income", "monthly salary"],
        "Salaried-Variable": ["variable income", "commission", "sales job"],
        "Homemaker": ["housewife", "homemaker", "stay at home"]
    },

    "savings_habit": {
        "Regular Saver": ["saving every month", "auto SIP", "monthly savings"],
        "Irregular Saver": ["saving sometimes", "bacha leta hoon", "some months", "kabhi kabhi save"],
        "No Savings": ["no savings", "can't save", "zero left", "kuch nahi bacha"],
        "Aspiring Saver": ["want to save", "start saving", "planning to save", "save karna chahta"],
        "Emergency-Fund Builder": ["emergency fund", "for emergencies", "medical fund", "bura waqt"]
    },

    "debt_behavior": {
        "EMI-Active": ["EMI", "installment", "loan payment"],
        "Heavy EMI Burden": ["too many loans", "heavy EMI", "loan pressure"],
        "Debt-Free": ["no EMI", "debt-free", "sabka khatam"],
        "Considering Credit Card": ["thinking credit card", "credit card lena hai"],
        "Credit Card Overuser": ["credit card bill", "missed payment", "over limit"]
    },

    "risk_appetite": {
        "Risk-Averse": ["safe investment", "don't want to lose", "FD is best", "paisa doob gaya toh"],
        "Risk-Open": ["some risk is fine", "calculated risk", "risk chalega"],
        "Risk-Seeking": ["high returns", "aggressive investment", "double paisa"],
        "Risk-Unaware": ["I don't know", "not sure about risk", "kya hota hai risk"]
    },

    "financial_dependency": {
        "Family-Supported": ["parents pay", "dad helps", "gift from papa", "ghar se paisa"],
        "Self-Supported": ["own income", "self-funded", "pocket money khatam"],
        "Dual Responsibility": ["supporting family", "take care of home too", "ghar bhi chalata hoon"]
    },

    "financial_awareness": {
        "Beginner": ["don't know", "basic questions", "paisa kaise bachaaye", "confused"],
        "Early Learner": ["SIP", "FD", "saving options", "PPF"],
        "Intermediate": ["mutual funds", "budgeting", "returns", "portfolio"],
        "Well-Informed": ["asset allocation", "diversification", "rebalancing", "net worth"]
    },

    "emotional_money_behavior": {
        "Instant Gratifier": ["impulse", "can't wait", "jaldi buy", "turant le liya"],
        "Security-Seeker": ["feel safe", "need stability", "secure future", "mental peace"],
        "Status-Spender": ["status", "prestige", "expensive", "show off", "Apple lena hai"],
        "Future Planner": ["long term", "retirement", "goal based", "future ke liye"]
    },

    "tone_preference": {
        "Gentle": ["I'm scared", "I don't know much", "confused", "nervous"],
        "Playful": ["chalo dekhte hain", "kuch seekhte hain", "lightly", "dekh lenge"],
        "Straightforward": ["tell me clearly", "no sugarcoating", "seedha bolo"],
        "Motivational": ["I want to change", "need discipline", "build something", "nayi journey"]
    },

    "goal_orientation": {
        "Short-Term Achiever": ["buying a phone", "6 months goal", "trip", "bike"],
        "Long-Term Builder": ["building wealth", "future savings", "retirement", "bada goal"],
        "No Clear Goal": ["no idea", "don’t know goal", "bas chal raha hai"]
    }
}

# -- Main Function
def extract_tags_from_onboarding(answers: list[str]) -> dict[str, str]:
    """
    Scans all onboarding answers and assigns the best-matching tag for each category.
    Falls back to 'Unknown' if no match is found.
    """
    tags = {}

    for category, tag_dict in TAG_RULES.items():
        found = False
        for tag, keywords in tag_dict.items():
            for ans in answers:
                ans_lower = ans.lower()
                for kw in keywords:
                    pattern = rf"\b{re.escape(kw.lower())}\b"
                    if re.search(pattern, ans_lower):
                        tags[category] = tag
                        found = True
                        break
                if found: break
            if found: break
        if category not in tags:
            tags[category] = "Unknown"

    return tags

# -- Persona Detection Function
def detect_persona(tags: dict[str, str]) -> str:
    """
    Determines the user's persona based on tag combinations.
    Returns one of the known persona names or 'Unknown Persona'.
    """
    persona_rules = {
        "Aspirational YOLO": {
            "income_status": "Salaried-Variable",
            "emotional_money_behavior": "Status-Spender",
            "risk_appetite": "Risk-Seeking"
        },
        "Dutiful Son/Daughter": {
            "financial_dependency": "Dual Responsibility",
            "emotional_money_behavior": "Security-Seeker",
            "financial_awareness": "Beginner"
        },
        "Silent Dreamer": {
            "income_status": "No Income",
            "emotional_money_behavior": "Instant Gratifier",
            "goal_orientation": "Short-Term Achiever"
        },
        "Cautious Climber": {
            "savings_habit": "Regular Saver",
            "risk_appetite": "Risk-Averse",
            "goal_orientation": "Long-Term Builder"
        },
        "Hustling Freelancer": {
            "income_status": "Freelancing",
            "risk_appetite": "Risk-Open",
            "financial_awareness": "Early Learner"
        },
        "Status Climber": {
            "income_status": "Salaried-Fixed",
            "debt_behavior": "Heavy EMI Burden",
            "emotional_money_behavior": "Status-Spender"
        },
        "Unaware Dabbler": {
            "financial_awareness": "Beginner",
            "risk_appetite": "Risk-Unaware",
            "goal_orientation": "No Clear Goal"
        }
    }

    for persona, conditions in persona_rules.items():
        if all(tags.get(key) == value for key, value in conditions.items()):
            return persona

    return "Unknown Persona"

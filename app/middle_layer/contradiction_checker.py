# File: lib/middle_layer/contradiction_checker.py

from transformers import pipeline
from typing import Union

# ✅ Load model ONCE
nli_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")

def should_include_tag(
    contradiction: float,
    entailment: float,
    neutral: float,
    contradiction_threshold: float = 0.9,
    entailment_threshold: float = 0.58
) -> bool:
    """
    Return True if tag should be included based on NLI confidence bands.
    """
    if contradiction >= contradiction_threshold:
        return False  # ❌ Strong contradiction
    if entailment >= entailment_threshold:
        return True   # ✅ Strong entailment
    if neutral >= 0.4 and contradiction < 0.2:
        return True   # ✅ Possibly valid, not contradicted
    return False      # ❌ Weak/conflicting signal

def is_contradiction_or_weak_entailment(
    premise: str,
    hypothesis: str,
    contradiction_threshold: float = 0.9,
    entailment_threshold: float = 0.58,
    return_scores: bool = False
) -> Union[bool, dict]:
    """
    Returns True if contradiction ≥ threshold OR entailment ≤ threshold.
    If return_scores=True, returns full label→score dictionary.
    """
    try:
        # ✅ CORRECT input format
        result = nli_pipeline({"text": premise, "text_pair": hypothesis}, top_k=None)

        # ✅ Flatten list of predictions if needed
        if isinstance(result, list):
            # Convert list to dictionary: {"entailment": 0.xx, "neutral": 0.xx, "contradiction": 0.xx}
            label_scores = {entry["label"].lower(): entry["score"] for entry in result}
        elif isinstance(result, dict):
            label_scores = {result["label"].lower(): result["score"]}
        else:
            raise ValueError("Unexpected NLI result format")

        contradiction = label_scores.get("contradiction", 0.0)
        entailment = label_scores.get("entailment", 0.0)
        neutral = label_scores.get("neutral", 0.0)

        print(f"\n🧠 NLI Scores → Premise: {premise} | Hypothesis: {hypothesis}")
        for label, score in label_scores.items():
            print(f"  → {label}: {round(score, 4)}")

        if return_scores:
            return label_scores

        return should_include_tag(
            contradiction, entailment, neutral,
            contradiction_threshold, entailment_threshold
        )

    except Exception as e:
        print(f"⚠️ NLI error for '{hypothesis}': {e}")
        return False if not return_scores else {
            "contradiction": 0.0,
            "entailment": 0.0,
            "neutral": 0.0
        }


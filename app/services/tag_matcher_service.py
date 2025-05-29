from typing import Dict

class TagMatcherService:
    def __init__(self, match_threshold=0.58):
        self.match_threshold = match_threshold

        # Entailment & contradiction cutoffs by tier
        self.tier1_entailment = 0.3
        self.tier2_entailment = 0.2
        self.tier2_contradiction = 0.25
        self.tier3_entailment = 0.05
        self.tier3_contradiction = 0.5

    def is_score_above_threshold(self, score: float) -> bool:
        return score >= self.match_threshold

    def is_score_valid(self, score: float) -> bool:
        """Alias for is_score_above_threshold() to align with external calls"""
        return self.is_score_above_threshold(score)

    def should_accept_tier1(self, entailment: float, contradiction: float) -> bool:
        return entailment >= self.tier1_entailment

    def should_accept_tier2(self, entailment: float, contradiction: float) -> bool:
        return entailment >= self.tier2_entailment and contradiction < self.tier2_contradiction

    def should_accept_tier3(self, entailment: float, contradiction: float) -> bool:
        return entailment >= self.tier3_entailment and contradiction <= self.tier3_contradiction

    def should_include(self, contradiction: float, entailment: float, neutral: float) -> bool:
        return self.should_accept_tier1(entailment, contradiction)

    def is_entailment_strong(self, entailment: float) -> bool:
        return entailment >= self.tier1_entailment

    def is_manual_contradiction(self, phrase: str, user_input: str) -> bool:
        contradiction_phrases = [
            "i help my parents financially", "i support my parents",
            "they depend on me", "parents depend on me",
            "take care of parents and my needs"
        ]
        user_triggers = [
            "rely on my parents", "my parents handle everything",
            "parents take care of all my expenses", "my parents pay",
            "my parents do everything", "mom handles my expenses"
        ]
        return any(p in phrase for p in contradiction_phrases) and any(t in user_input for t in user_triggers)

    def is_score_valid(self, score: float) -> bool:
        return score >= self.match_threshold

    def get_fallback_matches(self, user_input: str, matches: list) -> list:
        tiers = [
            {"entailment": self.tier2_entailment, "contradiction": self.tier2_contradiction, "label": "Tier 2"},
            {"entailment": self.tier3_entailment, "contradiction": self.tier3_contradiction, "label": "Tier 3"},
        ]

        from app.middle_layer.contradiction_checker import is_contradiction_or_weak_entailment
        from operator import itemgetter

        user_input_lower = user_input.lower()
        for tier in tiers:
            fallback_per_category = {}
            for match in matches:
                score = match["score"]
                if score < 0.5:
                    continue
                metadata = match["metadata"]
                tag = metadata.get("tag")
                category = metadata.get("category")
                phrase = metadata.get("original_phrase", "")
                phrase_lower = phrase.lower()

                try:
                    scores = is_contradiction_or_weak_entailment(user_input, phrase, return_scores=True)
                    entailment = scores.get("entailment", 0.0)
                    contradiction = scores.get("contradiction", 0.0)

                    if entailment >= tier["entailment"] and contradiction <= tier["contradiction"]:
                        current = fallback_per_category.get(category)
                        if not current or entailment > current["entailment"]:
                            fallback_per_category[category] = {
                                "category": category,
                                "tag": tag,
                                "matched_phrase": phrase,
                                "score": round(score, 4),
                                "entailment": entailment,
                                "tentative": True
                            }
                except Exception as e:
                    print(f"⚠️ Fallback NLI error for '{phrase}': {e}")
                    continue

            if fallback_per_category:
                print(f"✅ Fallback matches returned from {tier['label']}: {[f['tag'] for f in fallback_per_category.values()]}")
                return sorted(fallback_per_category.values(), key=itemgetter("score"), reverse=True)

        return []

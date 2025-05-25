import os
import sys
from typing import Dict
from operator import itemgetter

# Add 'lib' directory to path for service imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'lib')))

from dotenv import load_dotenv
import openai
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

from app.middle_layer.contradiction_checker import is_contradiction_or_weak_entailment
from services.tag_matcher_service import TagMatcherService  # fixed relative import

# Load environment variables
load_dotenv()


# API and model setup
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV", "us-east-1")
index_name = "semantic-tags"
embedding_model = "text-embedding-3-small"
embedding_dimensions = 1536
match_threshold = 0.58

# Initialize OpenAI and Pinecone clients
client = OpenAI(api_key=openai.api_key)
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)

# Initialize tag matcher service
tag_matcher = TagMatcherService(match_threshold)


def get_text_embedding(text: str):
    response = client.embeddings.create(
        input=[text],
        model=embedding_model
    )
    return response.data[0].embedding


def construct_clarification_prompt(user_input: str, matches: list) -> dict:
    top_phrases = []
    seen_phrases = set()

    for match in matches:
        phrase = match['metadata'].get('original_phrase', '')
        if phrase and phrase not in seen_phrases:
            top_phrases.append(phrase)
            seen_phrases.add(phrase)
        if len(top_phrases) == 3:
            break

    if not top_phrases:
        return {}

    if len(top_phrases) == 1:
        question = f"Just to clarify: would you say something like \"{top_phrases[0]}\"?"
    else:
        quoted = [f"\"{p}\"" for p in top_phrases]
        question = f"Just to clarify: would you say something like {', '.join(quoted[:-1])}, or {quoted[-1]}?"

    return {"question": question, "options": top_phrases}


def find_best_tag(user_input: str, top_k: int = 10, debug: bool = True) -> dict:
    query_vector = get_text_embedding(user_input)
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

    user_input_lower = user_input.lower()

    if debug:
        print("\n📊 FULL RAW Pinecone MATCHES:")
        for match in results['matches']:
            print(f"→ Score: {round(match['score'], 4)} | Tag: {match['metadata'].get('tag')} | Phrase: {match['metadata'].get('original_phrase')} | Category: {match['metadata'].get('category')}")

    best_per_category: Dict[str, dict] = {}

    for match in results['matches']:
        score = match['score']
        if not tag_matcher.is_score_valid(score):
            continue

        metadata = match['metadata']
        tag = metadata.get('tag')
        category = metadata.get('category')
        matched_phrase = metadata.get('original_phrase', '')
        matched_phrase_lower = matched_phrase.lower()

        # 🧠 NLI filtering
        try:
            scores = is_contradiction_or_weak_entailment(
                premise=user_input,
                hypothesis=matched_phrase,
                return_scores=True
            )
            contradiction = scores.get("contradiction", 0.0)
            entailment = scores.get("entailment", 0.0)
            neutral = scores.get("neutral", 0.0)

            if not tag_matcher.should_include(contradiction, entailment, neutral):
                print(f"⛔ Skipping Tag: {tag} | Phrase: {matched_phrase}")
                continue
        except Exception as e:
            print(f"⚠️ NLI error for '{matched_phrase}': {e}")
            continue

        if tag_matcher.is_manual_contradiction(matched_phrase_lower, user_input_lower):
            print(f"❌ Manual contradiction → Skipping Tag: {tag} | Phrase: {matched_phrase}")
            continue

        if not tag_matcher.is_entailment_strong(entailment):
            print(f"🟡 Skipping weak tag despite passing NLI → Tag: {tag} | Entailment: {entailment}")
            continue

        current_best = best_per_category.get(category)
        if not current_best or entailment > current_best['entailment']:
            best_per_category[category] = {
                "category": category,
                "tag": tag,
                "matched_phrase": matched_phrase,
                "score": round(score, 4),
                "entailment": entailment,
                "tentative": False
            }

    final_matches = sorted(best_per_category.values(), key=itemgetter("score"), reverse=True)
    if final_matches:
        return {"matches": final_matches, "fallback": False}

    # 🚨 Tier 1 didn't return anything → Try fallback logic
    print("⚠️ No strong matches found. Attempting fallback...")
    fallback_matches = tag_matcher.get_fallback_matches(user_input, results['matches'])
    if fallback_matches:
        return {"matches": fallback_matches, "fallback": True}

    # 🧠 Still nothing → suggest clarification
    print("❌ No fallback matches survived in any tier.")
    clarification_prompt = construct_clarification_prompt(user_input, results['matches'])
    return {
        "matches": [],
        "fallback": True,
        "clarification_prompt": clarification_prompt
    }
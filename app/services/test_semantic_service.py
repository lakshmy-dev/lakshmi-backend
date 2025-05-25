from semantic_service import get_semantic_tags

test_inputs = [
    "I try to save, but I often end up spending",
    "My parents pay rent but I buy groceries myself",
    "Not sure what I should do with my salary right now",
    "I’ve taken loans before, but I’m debt-free now",
    "I feel like I waste money but I also want financial security"
]

for test_input in test_inputs:
    print(f"\n📨 Testing input: {test_input}")
    result = get_semantic_tags(test_input)

    if isinstance(result, dict):
        tags = result.get("matches", [])
        fallback_used = result.get("fallback", False)
    else:
        tags = result
        fallback_used = False

    if not tags:
        print("❌ No tags returned.")
        continue

    if fallback_used:
        print("⚠️ Fallback was triggered and returned these tags:")
    else:
        print("✅ Primary match logic returned these tags:")

    seen_categories = set()
    duplicates = False

    for tag in tags:
        category = tag['category']
        if category in seen_categories:
            print(f"⚠️ Duplicate category detected: {category}")
            duplicates = True
        seen_categories.add(category)

        print(f"✅ Tag: {tag['tag']} | Category: {category} | Phrase: {tag['matched_phrase']} | Score: {tag['score']}")

    if not duplicates:
        print("🎯 All tags are unique per category.")

# File: lib/middle_layer/convert_to_semantic_format.py

import json
import os

# Full absolute input/output path
input_file = os.path.abspath("rules/master_rules.json")
output_file = os.path.abspath("lib/middle_layer/semantic_tag_examples.json")

def normalize_category(category: str) -> str:
    return category.lower().strip().replace(" ", "_")

with open(input_file, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

semantic_data = {}

print(f"✅ Loaded {len(raw_data)} rules from {input_file}")

for rule in raw_data:
    category_raw = rule.get("category")
    tag = rule.get("tag_to_assign")
    phrases = rule.get("keywords")

    if not category_raw or not tag or not phrases:
        print(f"⚠️ Skipping rule due to missing fields: {rule.get('rule_id', 'unknown')}")
        continue

    category = normalize_category(category_raw)

    print(f"🔍 Processing rule: {rule.get('rule_id')} | category: {category} | tag: {tag} | {len(phrases)} phrases")

    if category not in semantic_data:
        semantic_data[category] = {}

    if tag not in semantic_data[category]:
        semantic_data[category][tag] = []

    semantic_data[category][tag].extend(phrases)

# Remove duplicates
for cat in semantic_data:
    for tag in semantic_data[cat]:
        semantic_data[cat][tag] = list(set(semantic_data[cat][tag]))

# 🔐 Force write using absolute path + flush + close
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(semantic_data, f, indent=2, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())

print(f"✅ Semantic tag examples saved to: {output_file}")

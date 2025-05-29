# File: lib/middle_layer/test_semantic_query.py

import os
import openai
from pinecone import Pinecone
from openai import OpenAI

# --- Setup ---
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV") or "us-east-1"

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("semantic-tags")

# --- Input ---
user_input = input("🧠 Enter a sample user phrase: ")

# --- Embed user input ---
response = openai.embeddings.create(
    model="text-embedding-3-small",
    input=user_input
)
embedding = response.data[0].embedding

# --- Query Pinecone ---
results = index.query(vector=embedding, top_k=3, include_metadata=True)

print("\n🔍 Top Matching Tags:")
for match in results.matches:
    tag = match.metadata.get("tag")
    category = match.metadata.get("category")
    phrase = match.metadata.get("original_phrase")
    score = round(match.score, 4)
    print(f"→ [{score}] Tag: {tag} | Category: {category} | Matched Phrase: “{phrase}”")

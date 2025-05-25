# File: lib/middle_layer/upload_semantic_tags.py

import json
import os
import uuid
from time import sleep
from tqdm import tqdm
import openai
from pinecone import Pinecone, ServerlessSpec
from requests.exceptions import RequestException

# --- Setup your API keys ---
openai.api_key = os.getenv("OPENAI_API_KEY") or "sk-..."  # Replace with your real key
pinecone_api_key = os.getenv("PINECONE_API_KEY") or "your-pinecone-key"
pinecone_env = os.getenv("PINECONE_ENV") or "us-east-1"

# --- Init Pinecone client ---
pc = Pinecone(api_key=pinecone_api_key)

# --- Index Config ---
index_name = "semantic-tags"
embedding_model = "text-embedding-3-small"
batch_size = 100

# --- Create index if it doesn't exist ---
available_indexes = pc.list_indexes().names()
if index_name not in available_indexes:
    print(f"ℹ️ Index '{index_name}' not found. Creating it now...")
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=pinecone_env)
    )
else:
    print(f"✅ Index '{index_name}' found.")

index = pc.Index(index_name)

# --- Load semantic tag data ---
json_path = "lib/middle_layer/semantic_tag_examples.json"
if not os.path.exists(json_path):
    raise FileNotFoundError(f"❌ File not found: {json_path}")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Get embeddings ---
def embed_text(text: str) -> list[float]:
    try:
        response = openai.embeddings.create(
            model=embedding_model,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Embedding failed for '{text}': {e}")
        return []

# --- Upload in batches with retry and delay ---
def upload_batch(batch_data, retry=3):
    for attempt in range(retry):
        try:
            index.upsert(vectors=batch_data)
            return True
        except Exception as e:
            print(f"⚠️ Upload attempt {attempt + 1} failed: {e}")
            sleep(1)
    print("❌ Final upload failed after retries.")
    return False

# --- Build and upload vectors ---
batch = []
for category, tag_dict in tqdm(data.items(), desc="📦 Uploading to Pinecone"):
    for tag, phrases in tag_dict.items():
        for phrase in phrases:
            embedding = embed_text(phrase)
            if not embedding:
                continue

            vector_id = str(uuid.uuid4())
            batch.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "category": category,
                    "tag": tag,
                    "original_phrase": phrase
                }
            })

            if len(batch) >= batch_size:
                success = upload_batch(batch)
                batch = []
                sleep(0.5)

# Upload any remaining
if batch:
    upload_batch(batch)

print(f"\n✅ Upload complete to index: {index_name}")

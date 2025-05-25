import requests

SEMANTIC_API_URL = "http://localhost:8000/semantic/match"

def get_semantic_tags(user_input: str):
    try:
        print(f"📤 Sending to: {SEMANTIC_API_URL}")
        print(f"📨 Payload: {{'user_input': '{user_input}'}}")

        response = requests.post(
            SEMANTIC_API_URL,
            json={"user_input": user_input}
        )

        print(f"🔧 Status Code: {response.status_code}")
        print(f"📦 Raw Response: {response.text}")

        if response.status_code == 200:
            return response.json().get("matches", [])
        else:
            return []
    except Exception as e:
        print(f"❌ Error calling semantic API: {e}")
        return []


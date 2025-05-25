import os
import requests
from dotenv import load_dotenv
from app.prompt_builder import build_summary_prompt  # ✅ NEW IMPORT

load_dotenv()  # ✅ Load API key from .env

class ClaudeService:
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-opus-20240229"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def generate(self, prompt_data):
        """
        Generic method — used for free-form prompts.
        prompt_data: {
            "system": "...",
            "messages": [
                {"role": "user", "content": "..."}
            ]
        }
        """
        try:
            payload = {
                "model": self.model,
                "max_tokens": 500,
                "system": prompt_data["system"],
                "messages": prompt_data["messages"]
            }

            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()

            data = response.json()

            if "content" in data and isinstance(data["content"], list):
                for item in data["content"]:
                    if item.get("type") == "text":
                        return item.get("text", "").strip()

            return "Claude responded, but content was not in expected format."

        except requests.exceptions.HTTPError as http_err:
            print("Claude API HTTP Error:", response.status_code, response.text)
            return f"Claude API HTTP Error: {response.status_code}"

        except Exception as e:
            print("Claude API Error:", e)
            return "Summary unavailable due to Claude API error."

    def generate_summary(self, scenario_data, language="English", tone="calm"):
        """
        Summary-specific method — uses LakshmiTone Layer™ and prompt builder.
        """
        prompt_data = build_summary_prompt(
            scenario_data=scenario_data,
            language=language,
            tone=tone
        )
        return self.generate(prompt_data)

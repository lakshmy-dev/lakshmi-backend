import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class GPTService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt_data: dict, model: str = "gpt-4"):
        """
        Generate a response using OpenAI's Chat Completions API.

        prompt_data: {
            "system": "Lakshmi prompt with context...",
            "messages": [
                {"role": "user", "content": "..."},
                ...
            ]
        }
        """
        try:
            system_prompt = prompt_data.get("system", "")
            messages = prompt_data.get("messages", [])

            # 🧠 Validate format
            if not isinstance(system_prompt, str):
                raise ValueError("Invalid 'system' prompt format")
            if not isinstance(messages, list) or not all(isinstance(m, dict) for m in messages):
                raise ValueError("Invalid 'messages' format")

            all_messages = [{"role": "system", "content": system_prompt}] + messages

            # 🚀 Call OpenAI Chat Completion
            response = self.client.chat.completions.create(
                model=model,
                messages=all_messages,
                max_tokens=500,
                temperature=0.58,  # ✅ Updated to preferred creative/controlled balance
                timeout=30
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print("OpenAI API Error:", e)
            return "Summary unavailable due to OpenAI API error."

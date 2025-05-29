# File: app/services/gpt_service.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from app.utils.lakshmi_prompt_builder import build_lakshmi_prompt

load_dotenv()  # Load environment variables from .env

class GPTService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def generate(
        self,
        messages: list,
        tags: dict = {},
        emotions: dict = {},
        user_name: str = "You",
        scenario_type: str = None,
        inputs: dict = {},
        model: str = "gpt-4"
    ) -> str:
        """
        Generate a response using OpenAI's Chat Completions API.

        Args:
            messages: List of chat history messages.
            tags: Semantic tags (from Pinecone/NLI).
            emotions: Detected emotion scores.
            user_name: Optional name for personalization.
            scenario_type: Optional financial goal context.
            inputs: Optional financial inputs (age, savings, etc.)
        """
        try:
            # ✅ Build Lakshmy's tone-rich prompt
            prompt_data = build_lakshmi_prompt(
                messages=messages,
                tags=tags,
                emotions=emotions,
                user_name=user_name,
                scenario_type=scenario_type,
                inputs=inputs
            )

            all_messages = [{"role": "system", "content": prompt_data["system"]}] + prompt_data["messages"]

            response = self.client.chat.completions.create(
                model=model,
                messages=all_messages,
                max_tokens=500,
                temperature=0.58,
                timeout=30
            )
            print(f"💬 GPT content type: {type(response.choices[0].message.content)}")
            print(f"💬 GPT raw: {response.choices[0].message.content}")


            return str(response.choices[0].message.content).strip()

        except Exception as e:
            print("❌ OpenAI API Error:", e)
            return "Summary unavailable due to OpenAI API error."

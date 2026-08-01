import os

import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_URL = "https://api.openai.com/v1/responses"


def _response_text(data):
    if data.get("output_text"):
        return data["output_text"].strip()

    text_parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                text_parts.append(text)

    return "\n".join(text_parts).strip()


class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("REASONING_MODEL")
        self.reasoning_effort = os.getenv("REASONING_EFFORT")

    def create_financial_report(self, prompt):
        if not self.api_key:
            raise ValueError("Missing OPENAI_API_KEY")

        if not self.model:
            raise ValueError("Missing REASONING_MODEL")

        payload = {
            "model": self.model,
            "instructions": (
                "You are a careful financial analyst. Use only the provided "
                "price data and news. Do not invent facts. This is not "
                "financial advice."
            ),
            "input": prompt,
            "max_output_tokens": 1200,
            "store": False,
        }

        if self.reasoning_effort:
            payload["reasoning"] = {
                "effort": self.reasoning_effort,
            }

        response = requests.post(
            OPENAI_API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        response.raise_for_status()

        data = response.json()
        report = _response_text(data)

        if not report:
            raise ValueError("OpenAI returned an empty report")

        return {
            "report": report,
            "model": data.get("model", self.model),
            "response_id": data.get("id"),
            "usage": data.get("usage"),
        }

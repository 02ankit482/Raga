import os
import requests
from dotenv import load_dotenv

from app.rag.constants import (
    GENERATION_MODEL_NAME,
    MAX_NEW_TOKENS,
    TEMPERATURE,
)

load_dotenv()

_HF_API_TOKEN = os.getenv("HF_API_TOKEN")
_ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"


def generate_answer(context: str, question: str) -> str:
    if not _HF_API_TOKEN:
        return (
            "Error: HF_API_TOKEN is not set. "
            "Please add it to your .env file."
        )

    prompt = f"""
You are a friendly and helpful AI assistant for students.

Your job:
- Answer questions using ONLY the provided context
- Be clear, concise, and polite
- Never answer unusual questions that are not related to the context, just casually state that you cannot answer as it is not related to docs provided.
- If the answer is not present in the context, say:
  "I cannot answer this based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
""".strip()


    headers = {
        "Authorization": f"Bearer {_HF_API_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GENERATION_MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": MAX_NEW_TOKENS,
        "temperature": TEMPERATURE,
    }

    try:
        response = requests.post(
            _ROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
    except Exception as e:
        return f"Error: HF API request failed: {e}"

    try:
        result = response.json()
    except Exception:
        return f"Error: Invalid HF response: {response.text}"

    if response.status_code not in (200, 201):
        return f"Error: {result.get('error', response.text)}"

    try:
        return result["choices"][0]["message"]["content"]
    except Exception:
        return f"Error: Unexpected HF response format: {result}"

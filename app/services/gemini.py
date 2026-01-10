import os
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.0-flash-001"

# JSON schema for response
ANALYSIS_SCHEMA = {
    "type": "object",
    "required": ["intent", "urgency", "summary", "suggested_actions"],
    "properties": {
        "intent": {"type": "string"},
        "urgency": {
            "type": "string",
            "enum": ["low", "medium", "high"]
        },
        "summary": {"type": "string"},
        "suggested_actions": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

def analyze_content_with_gemini(content_type: str, content: dict) -> dict:
    prompt = f"""
    Analyze the following {content_type}.

    Content:
    {content}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
            response_json_schema=ANALYSIS_SCHEMA,
        ),
    )

    # SAFE: already validated JSON
    return response.parsed

# for ai reply generation

def generate_reply_with_gemini(payload: dict):
    email = payload["original_email"]
    context = payload.get("context", {})
    tone = payload.get("tone", "professional")

    prompt = f"""
You are an AI assistant drafting email replies.

Write a {tone} reply to the following email.

Email:
Subject: {email.get("subject")}
Body: {email.get("body")}

Return ONLY the reply text.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.3}
    )

    return {
        "reply": response.text.strip()
    }




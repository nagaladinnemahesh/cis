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
            "minItems":0,
            "maxItems":2,
            "items": {"type": "string"}
        }
    }
}

def normalize_suggested_action(actions: list[str], intent: str) -> str:
    """
    Convert Gemini's suggested_actions array into ONE clean sentence
    suitable for direct UI display.
    """

    if not actions:
        return "Review and respond if needed."

    action = actions[0].strip()

    # Safety: avoid very long / verbose actions
    if len(action.split()) > 14:
        return "Review and respond accordingly."

    if not action.endswith("."):
        action += "."

    return action


def analyze_content_with_gemini(
    content_type: str,
    content: dict,
    contexts: list | None = None
) -> dict:

    context_block = ""
    if contexts:
        context_block = "\n\nPrevious related analyses:\n"
        for i, ctx in enumerate(contexts, start=1):
            context_block += (
                f"{i}. Intent: {ctx.get('intent')}, "
                f"Urgency: {ctx.get('urgency')}, "
                f"Summary: {ctx.get('summary')}\n"
            )

    prompt = f"""
You are an intelligent email analysis assistant.

Use the previous related analyses ONLY as reference patterns.
Do NOT copy them verbatim.
Use them to improve intent detection and urgency classification.

{context_block}

Analyze the following {content_type} and return ONLY valid JSON
that strictly follows the given schema.

Rules:
- intent: short snake_case string
- urgency: one of low | medium | high
- summary: ONE short sentence (max 20 words)
- suggested_actions:
  - Return 1 to 3 SHORT action sentences
  - Do NOT over-explain
  - If no action is required, return:
    ["No action required at this time."]

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

    analysis = response.parsed

    # Normalize suggested action for UI
    analysis["suggested_action"] = normalize_suggested_action(
        analysis.get("suggested_actions", []),
        analysis["intent"]
    )

    analysis.pop("suggested_actions", None)

    print("FINAL ANALYSIS SENT TO API:", analysis)

    return analysis



def generate_reply_with_gemini(payload: dict):
    email = payload["original_email"]
    analysis = payload.get("analysis", {})
    tone = payload.get("tone", "professional")

    prompt = f"""
You are a professional email assistant.

Context:
- Intent: {analysis.get("intent")}
- Urgency: {analysis.get("urgency")}
- Summary: {analysis.get("summary")}

Write a {tone} reply to the email below.

Email:
Subject: {email.get("subject")}
Body: {email.get("body")}

Rules:
- Write only the email body
- Be clear, polite, and human
- Do NOT include subject
- Do NOT add placeholders
- Do NOT explain your reasoning

Return only plain text.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.3}
    )

    return {"reply": response.text.strip()}

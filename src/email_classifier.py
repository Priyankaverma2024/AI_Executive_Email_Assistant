"""
Classifies an incoming email into an intent category using Gemini.
This lets the reply generator use a category-specific strategy/tone,
and lets you auto-skip categories you don't want the agent touching
(e.g. spam, newsletters).
"""
import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

CATEGORIES = [
    "meeting_request",
    "follow_up",
    "task_assignment",
    "question",
    "complaint",
    "introduction_networking",
    "newsletter_promotional",
    "other",
]


def classify_email(subject: str, body: str) -> dict:
    """
    Returns: {"category": str, "urgency": "low"|"medium"|"high", "needs_reply": bool}
    """
    prompt = f"""Classify this email. Respond with ONLY valid JSON, no other text.

Categories: {", ".join(CATEGORIES)}

Email subject: {subject}
Email body: {body[:2000]}

Return JSON in exactly this format:
{{"category": "<one category>", "urgency": "low|medium|high", "needs_reply": true|false}}"""

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0, "max_output_tokens": 200},
    )

    raw_text = response.text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # Fail-safe default if the model returns malformed JSON
        return {"category": "other", "urgency": "low", "needs_reply": True}

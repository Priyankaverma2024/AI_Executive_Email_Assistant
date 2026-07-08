"""
Generates a professional draft reply using Gemini, tailored to the
email's category/urgency and your personal signature/tone.
"""
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, YOUR_NAME, YOUR_ROLE, YOUR_SIGNATURE_BLOCK

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# Category-specific instructions help Gemini match the right tone/structure
CATEGORY_GUIDANCE = {
    "meeting_request": "Confirm availability or propose 2-3 alternative time slots. Be concise.",
    "follow_up": "Acknowledge the follow-up, give a clear status update, and state next steps.",
    "task_assignment": "Confirm you've understood the task, ask any clarifying question if needed, and give an estimated timeline.",
    "question": "Answer directly and clearly. If you don't have enough information to answer, say so and ask what's needed.",
    "complaint": "Be empathetic, acknowledge the issue without over-apologizing, and outline a concrete next step.",
    "introduction_networking": "Be warm and professional, briefly say something relevant, and suggest a next step (call/meeting) if appropriate.",
    "newsletter_promotional": "Politely decline or note no reply needed.",
    "other": "Write a professional, helpful, and concise reply.",
}


def generate_reply(email: dict, classification: dict, extra_context: str = "") -> str:
    """
    email: {"subject", "sender", "body"}
    classification: {"category", "urgency", "needs_reply"}
    extra_context: optional freeform info you want the model to consider
                   (e.g. "I'm on leave next week", "Tell them the report is delayed")
    """
    category = classification.get("category", "other")
    guidance = CATEGORY_GUIDANCE.get(category, CATEGORY_GUIDANCE["other"])

    prompt = f"""You are drafting a professional email reply on behalf of {YOUR_NAME}, \
a {YOUR_ROLE}. Write in a clear, courteous, professional tone -- concise, no fluff, \
no over-apologizing, no excessive exclamation marks.

Original email:
From: {email['sender']}
Subject: {email['subject']}
Body:
{email['body'][:3000]}

Category: {category} (urgency: {classification.get('urgency', 'low')})
Reply strategy: {guidance}

{"Additional context to factor in: " + extra_context if extra_context else ""}

Write ONLY the email reply body (no subject line, no explanation of your choices). \
Do not include a signature block -- that will be added separately."""

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.4, "max_output_tokens": 600},
    )

    reply_body = response.text.strip()
    return f"{reply_body}\n\n{YOUR_SIGNATURE_BLOCK}"

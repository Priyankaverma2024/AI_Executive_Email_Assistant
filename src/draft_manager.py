"""
Creates a DRAFT reply in Gmail (does NOT send). You always review
and hit "Send" yourself -- keeps a human in the loop.
"""
import base64
from email.mime.text import MIMEText


def create_draft_reply(service, original_message: dict, reply_text: str):
    """
    original_message: {"id", "thread_id", "subject", "sender"}
    reply_text: the generated reply body
    """
    subject = original_message["subject"]
    if not subject.lower().startswith("re:"):
        subject = f"Re: {subject}"

    message = MIMEText(reply_text)
    message["to"] = original_message["sender"]
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    draft_body = {
        "message": {
            "raw": raw,
            "threadId": original_message["thread_id"],
        }
    }

    draft = (
        service.users()
        .drafts()
        .create(userId="me", body=draft_body)
        .execute()
    )
    return draft

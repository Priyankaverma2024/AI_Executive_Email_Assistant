"""
Fetches unread emails from Gmail and extracts clean, readable text
(strips HTML, signatures noise, etc. at a basic level).
"""
import base64
from email.mime.text import MIMEText


def list_unread_messages(service, max_results=10):
    """Returns a list of unread message metadata (id, threadId)."""
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX", "UNREAD"], maxResults=max_results)
        .execute()
    )
    return results.get("messages", [])


def get_message_detail(service, msg_id):
    """Fetches full message content and parses sender, subject, and body."""
    msg = (
        service.users()
        .messages()
        .get(userId="me", id=msg_id, format="full")
        .execute()
    )

    headers = msg["payload"].get("headers", [])
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(no subject)")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "(unknown sender)")

    body = _extract_body(msg["payload"])

    return {
        "id": msg_id,
        "thread_id": msg["threadId"],
        "subject": subject,
        "sender": sender,
        "body": body,
    }


def _extract_body(payload):
    """Recursively extracts plain-text body from a Gmail message payload."""
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            # Recurse into nested parts (multipart/alternative etc.)
            if "parts" in part:
                result = _extract_body(part)
                if result:
                    return result
        return ""
    else:
        data = payload.get("body", {}).get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        return ""

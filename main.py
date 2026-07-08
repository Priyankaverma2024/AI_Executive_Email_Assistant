"""
Personal Email Reply Agent
---------------------------
Pipeline: fetch unread emails -> classify intent -> generate draft reply -> save as Gmail draft.

Run:
    python main.py

Nothing is ever auto-sent. Check your Gmail Drafts folder to review and send.
"""
from src.gmail_auth import get_gmail_service
from src.email_fetcher import list_unread_messages, get_message_detail
from src.email_classifier import classify_email
from src.reply_generator import generate_reply
from src.draft_manager import create_draft_reply
from config import MAX_EMAILS_PER_RUN

# Categories the agent will skip (no draft created)
SKIP_CATEGORIES = {"newsletter_promotional"}


def run():
    print("Authenticating with Gmail...")
    service = get_gmail_service()

    print(f"Fetching up to {MAX_EMAILS_PER_RUN} unread emails...")
    messages = list_unread_messages(service, max_results=MAX_EMAILS_PER_RUN)

    if not messages:
        print("No unread emails found.")
        return

    for msg_ref in messages:
        email = get_message_detail(service, msg_ref["id"])
        print(f"\n--- Processing: '{email['subject']}' from {email['sender']} ---")

        classification = classify_email(email["subject"], email["body"])
        print(f"Classified as: {classification}")

        if classification["category"] in SKIP_CATEGORIES or not classification.get("needs_reply", True):
            print("Skipping (no reply needed / excluded category).")
            continue

        reply_text = generate_reply(email, classification)
        print(f"Generated reply:\n{reply_text}\n")

        draft = create_draft_reply(service, email, reply_text)
        print(f"Draft saved in Gmail (draft id: {draft['id']}). Review before sending.")

    print("\nDone. All drafts are waiting in your Gmail Drafts folder for review.")


if __name__ == "__main__":
    run()

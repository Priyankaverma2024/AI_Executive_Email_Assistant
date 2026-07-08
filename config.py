"""
Central configuration for the Email AI Agent.
Loads all settings from environment variables (.env file).
"""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUR_NAME = os.getenv("YOUR_NAME", "Your Name")
YOUR_ROLE = os.getenv("YOUR_ROLE", "Data Science Intern")
YOUR_SIGNATURE_BLOCK = os.getenv(
    "YOUR_SIGNATURE_BLOCK", "Best regards,\nYour Name"
).replace("\\n", "\n")
MAX_EMAILS_PER_RUN = int(os.getenv("MAX_EMAILS_PER_RUN", "10"))

# Gmail API scopes - modify (not send) so the agent can only create/edit drafts,
# never send mail on its own.
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
]

# Model to use for all Gemini calls (free tier model)
GEMINI_MODEL = "gemini-2.5-flash"

# Paths
CREDENTIALS_PATH = "credentials.json"   # downloaded from Google Cloud Console
TOKEN_PATH = "token.json"               # auto-generated after first login

if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY is missing. Copy .env.example to .env and fill it in."
    )

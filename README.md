# Personal AI Email Reply Agent

An agent that reads your unread Gmail, classifies each email's intent, drafts a
professional reply in your voice using Gemini, and saves it to **Drafts** —
never auto-sends. You always review before hitting Send.

## How it works

```
Gmail Inbox (unread)
      │
      ▼
email_fetcher.py    -> pulls sender, subject, body
      │
      ▼
email_classifier.py -> Gemini labels intent (meeting_request, follow_up, complaint, etc.)
      │
      ▼
reply_generator.py  -> Gemini drafts a reply, tone matched to category + your signature
      │
      ▼
draft_manager.py    -> saves reply as a Gmail Draft (human-in-the-loop, safe by design)
```

## Folder structure

```
email-ai-agent/
├── main.py                  # orchestrates the full pipeline
├── config.py                 # loads settings from .env
├── requirements.txt
├── .env.example               # copy to .env and fill in
├── credentials.json           # you download this from Google Cloud (see below)
├── token.json                 # auto-created after first login
└── src/
    ├── gmail_auth.py           # Gmail OAuth login
    ├── email_fetcher.py        # fetch + parse unread emails
    ├── email_classifier.py     # Claude-based intent classification
    ├── reply_generator.py      # Claude-based reply drafting
    └── draft_manager.py        # saves draft back to Gmail
```

## Setup (one-time)

### 1. Install dependencies
```bash
cd email-ai-agent
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get a Gemini API key (free, no credit card)
- Go to https://ai.google.dev/
- Click **"Get API key"** (top right, or under "Get started")
- Sign in with your Google account and click **Create API key**
- Copy the key — this uses Google's free tier (Gemini 2.5 Flash), no billing required

### 3. Get Gmail API credentials
1. Go to https://console.cloud.google.com/ and create a new project.
2. Enable the **Gmail API** (APIs & Services → Library → search "Gmail API" → Enable).
3. Go to APIs & Services → Credentials → Create Credentials → **OAuth client ID**.
   - Application type: **Desktop app**
4. Download the JSON file, rename it `credentials.json`, and place it in the
   project root (same folder as `main.py`).
5. On the OAuth consent screen, add your own Gmail address as a **test user**
   (required while the app is in "Testing" mode).

### 4. Configure environment variables
```bash
cp .env.example .env
```
Then edit `.env` and fill in your `GEMINI_API_KEY`, name, role, and signature.

### 5. Run it
```bash
python main.py
```
First run opens a browser window — log in with the Gmail account you want the
agent to manage and click Allow. After that, `token.json` is cached and you
won't need to log in again.

Generated replies appear in your **Gmail Drafts** folder — open Gmail, review,
edit if needed, and click Send yourself.

## Customizing the agent

- **Add/remove categories** → edit `CATEGORIES` in `src/email_classifier.py`
  and matching entries in `CATEGORY_GUIDANCE` in `src/reply_generator.py`.
- **Skip certain categories entirely** → edit `SKIP_CATEGORIES` in `main.py`.
- **Match your writing style more closely** → paste 3-5 of your own past sent
  emails into the prompt in `reply_generator.py` as few-shot examples; Claude
  will mimic your phrasing patterns.
- **Auto-run on a schedule** → wrap `main.py` in a cron job (Linux/Mac) or
  Task Scheduler (Windows), e.g. every 30 minutes.
- **Auto-send instead of draft** (not recommended while testing) → in
  `draft_manager.py`, use `service.users().messages().send()` instead of
  `.drafts().create()`. Only do this once you fully trust the output.

## Why draft-only, not auto-send?

An LLM can misread sarcasm, miss context from a longer thread, or hallucinate
a fact. Keeping a human-in-the-loop review step is standard practice for any
agent that touches external communication — this is also a good talking
point in interviews about responsible agent design.

## Extending this project (portfolio ideas)

- Add a vector store (e.g. Chroma) of your past sent emails for true
  style-matching via retrieval-augmented generation.
- Add a Streamlit dashboard to review/approve drafts outside Gmail.
- Log every classification + draft to a CSV/database and build a small
  evaluation set to measure classification accuracy over time.
- Add Slack/Teams integration to notify you when a high-urgency email arrives.

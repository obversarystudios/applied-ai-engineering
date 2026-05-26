# calling-an-api

**Source:** `Intro to AI Engineering with Python (1_6) – ChatGPT and the OpenAI API – Finxter Academy.pdf`

## Goal

Call the OpenAI Chat Completions API from Python with an API key loaded from `.env` (no hardcoded secrets).

## Layout

```text
calling-an-api/
  .env.example
  .gitignore
  chat_gpt_request.py
  requirements.txt
```

## Setup and run

```bash
cd projects/calling-an-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: OPENAI_API_KEY=sk-...
python chat_gpt_request.py
```

You should see a one-sentence assistant reply printed to the terminal.

## Core pattern (from lesson)

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = CLIENT.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)
print(response.choices[0].message.content)
```

## Dependencies

- `openai`, `python-dotenv`

## Next modules

- [`chat-completions-summarizer`](../chat-completions-summarizer/) — system prompt + file input
- [`api-keys-and-env`](../api-keys-and-env/) — key setup only (do this first if you skipped it)

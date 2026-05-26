# calling-an-api

**Source:** `Intro to AI Engineering with Python (1_6) – ChatGPT and the OpenAI API – Finxter Academy.pdf`

## Goal

Call the OpenAI Chat Completions API from Python with an API key loaded from `.env` (no hardcoded secrets).

## Suggested layout

```text
calling-an-api/
  .env                 # OPENAI_API_KEY=sk-...
  .gitignore           # ignore .env
  chat_gpt_request.py  # CLIENT + messages + print response
  requirements.txt     # openai, python-dotenv
```

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

- `pip install openai python-dotenv`

## Next modules

- `chat-completions-summarizer` — system prompt + file input
- `api-keys-and-env` — key setup only (prerequisite detail)

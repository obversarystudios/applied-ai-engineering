# api-keys-and-env

**Source PDF(s):** Intro (1/6) — see [`../../INDEX.md`](../../INDEX.md)

## Goal

Create and store OpenAI (and later Google) API keys safely in `.env`; never commit secrets.

## Layout

```text
api-keys-and-env/
  .env.example          # copy → .env
  .gitignore            # ignores .env and .venv/
  requirements.txt
  verify_env.py         # checks keys load without printing values
```

## Setup and run

```bash
cd projects/api-keys-and-env
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set OPENAI_API_KEY=sk-...
python verify_env.py
```

Expected output when configured:

```text
ok  OPENAI_API_KEY — OpenAI Chat, images, audio (most modules)

All checked keys are set.
```

## Dependencies

- `python-dotenv`

## Next

- [`calling-an-api`](../calling-an-api/) — first real API call

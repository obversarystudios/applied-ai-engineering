# chat-completions-summarizer

**Source PDF(s):** Intro (1/6) — see [`../../INDEX.md`](../../INDEX.md)

## Goal

Summarize text from a file using system + user messages and `gpt-4o-mini`.

## Layout

```text
chat-completions-summarizer/
  .env.example
  .gitignore
  chat_gpt_request.py
  text_to_summarize.txt    # edit this with your own source text
  requirements.txt
```

## Setup and run

```bash
cd projects/chat-completions-summarizer
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: OPENAI_API_KEY=sk-...
python chat_gpt_request.py
```

The script prints a preview of the input file, then **three bullet points** from the model.

## Customize

Replace the contents of `text_to_summarize.txt` with any paragraph you want summarized.

## Dependencies

- `openai`, `python-dotenv`

## Next

- [`langchain-prompts-and-chains`](../langchain-prompts-and-chains/)

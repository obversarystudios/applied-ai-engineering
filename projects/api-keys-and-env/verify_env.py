"""Verify OPENAI_API_KEY is loaded from .env (Recipe A)."""
import os

from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
if key:
    print("ok: OPENAI_API_KEY is set")
else:
    print("missing: add OPENAI_API_KEY=sk-... to .env")
    raise SystemExit(1)

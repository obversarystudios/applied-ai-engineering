"""Summarize text from a file via Chat Completions (Recipe B)."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Set OPENAI_API_KEY in .env (see .env.example)")
    sys.exit(1)

CLIENT = OpenAI(api_key=api_key)

text_path = Path(__file__).parent / "text_to_summarize.txt"
if not text_path.is_file():
    print(f"Missing input file: {text_path}")
    sys.exit(1)

user_text = text_path.read_text(encoding="utf-8").strip()
print(f"--- Input ({len(user_text)} chars from {text_path.name}) ---\n")
print(user_text[:400] + ("..." if len(user_text) > 400 else ""))
print("\n--- Summary ---\n")

response = CLIENT.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "You summarize technical text clearly. "
                "Respond with exactly three bullet points."
            ),
        },
        {"role": "user", "content": user_text},
    ],
)

print(response.choices[0].message.content)

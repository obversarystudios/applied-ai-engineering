"""Minimal OpenAI Chat Completions call (Recipe B)."""
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Set OPENAI_API_KEY in .env (see .env.example)")
    sys.exit(1)

CLIENT = OpenAI(api_key=api_key)

response = CLIENT.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Reply in one short sentence."},
    ],
)

print(response.choices[0].message.content)

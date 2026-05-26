"""Summarize text from a file via Chat Completions (Recipe B)."""
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

text_path = Path(__file__).parent / "text_to_summarize.txt"
user_text = text_path.read_text(encoding="utf-8").strip()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You summarize text clearly in three bullet points.",
        },
        {"role": "user", "content": user_text},
    ],
)
print(response.choices[0].message.content)

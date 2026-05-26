"""Verify API keys load from .env (Recipe A)."""
import os
import sys

from dotenv import load_dotenv

load_dotenv()

KEYS = {
    "OPENAI_API_KEY": "OpenAI Chat, images, audio (most modules)",
}


def main() -> None:
    missing = []
    for name, hint in KEYS.items():
        value = os.getenv(name)
        if value and value.strip() and not value.startswith("sk-your"):
            print(f"ok  {name} — {hint}")
        else:
            print(f"MISSING  {name} — {hint}")
            missing.append(name)

    if missing:
        print("\nCreate .env from .env.example and add your keys.")
        sys.exit(1)
    print("\nAll checked keys are set.")


if __name__ == "__main__":
    main()

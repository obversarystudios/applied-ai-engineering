"""Generate an image from a text prompt.

Default model is configurable via OPENAI_IMAGE_MODEL.
We request base64 output and save a PNG under output/.
"""

import base64
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY in .env (see .env.example)")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""
    if not prompt:
        prompt = "A clean flat vector icon of a rocket ship, minimal, white background"

    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
    size = os.getenv("OPENAI_IMAGE_SIZE", "1024x1024")

    client = OpenAI(api_key=api_key)

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"image_{ts}.png"

    # Prefer base64 so we don't rely on URL downloading.
    resp = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        response_format="b64_json",
    )

    b64 = resp.data[0].b64_json
    if not b64:
        raise RuntimeError("No image data returned (b64_json was empty)")

    out_path.write_bytes(base64.b64decode(b64))

    print(f"model: {model}")
    print(f"size: {size}")
    print(f"saved: {out_path}")


if __name__ == "__main__":
    main()

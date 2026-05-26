# Python cheatsheet — applied applications & deployments

Modular reference for **building**, **running**, and **shipping** small Python apps (API clients, demos, batch jobs). Pair with [`projects/README.md`](projects/README.md) for Finxter module recipes and [`INDEX.md`](INDEX.md) for lesson artifacts.

---

## How to read and extend this file

Every **module** below uses the same headers. Copy the [blank module template](#blank-module-template) when you add a new pattern.

| Header | What it holds |
|--------|----------------|
| **Purpose** | One-line outcome |
| **When** | Situations where this pattern applies |
| **Layout** | Files and folders |
| **Code** | Minimal working patterns (placeholders, no real secrets) |
| **Run locally** | Commands in an activated `.venv` |
| **Deploy** | How this shape maps to production-ish hosting |
| **Pitfalls** | Common failures |

**Module index**

| ID | Module | Topic |
|----|--------|--------|
| M01 | [Project skeleton](#module-m01-project-skeleton) | venv, layout, entrypoints |
| M02 | [Secrets and config](#module-m02-secrets-and-config) | `.env`, env vars |
| M03 | [CLI script](#module-m03-cli-script) | `argparse`, `__main__` |
| M04 | [HTTP API client](#module-m04-http-api-client) | OpenAI-style clients |
| M05 | [Files and artifacts](#module-m05-files-and-artifacts) | read/write, downloads |
| M06 | [LangChain app](#module-m06-langchain-app) | chains, invoke |
| M07 | [Gradio demo](#module-m07-gradio-demo) | Blocks UI |
| M08 | [Streamlit app](#module-m08-streamlit-app) | `app.py` UI |
| M09 | [Batch / pipeline job](#module-m09-batch--pipeline-job) | `main()`, steps |
| M10 | [Dependencies](#module-m10-dependencies) | `requirements.txt`, pins |
| M11 | [Logging and errors](#module-m11-logging-and-errors) | observability |
| M12 | [Config by environment](#module-m12-config-by-environment) | dev vs prod |
| M13 | [Docker deploy](#module-m13-docker-deploy) | container pattern |
| M14 | [Process managers](#module-m14-process-managers) | systemd, cloud run |
| M15 | [Pre-deploy checklist](#module-m15-pre-deploy-checklist) | ship safely |

---

## Module: M01 — Project skeleton

### Purpose

Repeatable folder + virtualenv so each app is isolated and runnable.

### When

Starting any new script, demo, or capstone under `projects/<name>/`.

### Layout

```text
my-app/
  .venv/                 # gitignored
  .env                   # gitignored
  .gitignore
  requirements.txt
  README.md              # goal, run command, deps
  src/                   # optional; flat root is fine for lessons
    __init__.py          # empty ok
    main.py              # or chat_gpt_request.py, app.py, etc.
  output/                # generated artifacts
  tests/                 # optional
    test_main.py
```

### Code

```python
# src/main.py — minimal entry
def main() -> None:
    print("ok")


if __name__ == "__main__":
    main()
```

`.gitignore` minimum:

```text
.env
.venv/
__pycache__/
*.pyc
output/
.DS_Store
```

### Run locally

```bash
cd my-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main          # if package layout
# or
python main.py              # if flat layout
```

### Deploy

Same tree ships to a VM, container, or PaaS; only env vars and start command change.

### Pitfalls

- Committing `.env` or `.venv/`
- Running `pip install` globally instead of inside `.venv`
- No `if __name__ == "__main__"` guard → accidental import side effects

---

## Module: M02 — Secrets and config

### Purpose

Load API keys and settings without hardcoding secrets in source.

### When

Any cloud API (OpenAI, Gemini), or deploy target that injects env vars.

### Layout

```text
.env                 # local only
.env.example         # committed; keys as placeholders
config.py            # optional thin wrapper
```

### Code

`.env.example` (commit this):

```text
OPENAI_API_KEY=sk-replace-me
GOOGLE_API_KEY=replace-me
APP_ENV=development
```

`config.py`:

```python
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    app_env: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            app_env=os.getenv("APP_ENV", "development"),
        )


def require_openai_key(settings: Settings) -> str:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing")
    return settings.openai_api_key
```

### Run locally

```bash
cp .env.example .env
# edit .env with real keys
python -c "from config import Settings; print(Settings.from_env().app_env)"
```

### Deploy

Set secrets in the host dashboard (Render, Fly, Railway, Lambda env, K8s Secret). **Never** bake keys into the image. Use `.env.example` as documentation only.

### Pitfalls

- `load_dotenv()` not called before `os.getenv`
- Logging or printing full API keys
- Same `.env` committed to git

---

## Module: M03 — CLI script

### Purpose

Script with arguments for local runs, cron, and CI.

### When

One-off tools, batch steps, capstone `main.py` orchestrators.

### Layout

```text
main.py
```

### Code

```python
import argparse
import sys


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run pipeline step")
    p.add_argument("--topic", required=True, help="Input topic")
    p.add_argument("--out-dir", default="output", help="Output directory")
    p.add_argument("--dry-run", action="store_true", help="Skip API calls")
    return p.parse_args(argv)


def run(topic: str, out_dir: str, dry_run: bool) -> int:
    if dry_run:
        print(f"[dry-run] would process: {topic} -> {out_dir}")
        return 0
    # real work here
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run(args.topic, args.out_dir, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
```

### Run locally

```bash
python main.py --topic "AI memes" --dry-run
python main.py --topic "AI memes" --out-dir output
```

### Deploy

Cron: `0 * * * * cd /app && /app/.venv/bin/python main.py --topic "..." >> /var/log/app.log 2>&1`

### Pitfalls

- No exit codes → hard to monitor failures
- Required args without `--help` text

---

## Module: M04 — HTTP API client

### Purpose

Thin wrapper around a vendor SDK with env-based auth.

### When

OpenAI chat, images, TTS, Whisper, Gemini, etc.

### Layout

```text
chat_gpt_request.py
# or generate_image.py, simple_gemini_request.py
```

### Code

```python
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat(user: str, system: str = "You are a helpful assistant.") -> str:
    resp = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content or ""


if __name__ == "__main__":
    print(chat("Hello!"))
```

Image (DALL·E) call shape:

```python
result = CLIENT.images.generate(
    model="dall-e-3",
    prompt="a friendly robot",
    size="1024x1024",
    n=1,
)
url = result.data[0].url
```

### Run locally

```bash
pip install openai python-dotenv
python chat_gpt_request.py
```

### Deploy

- Set `OPENAI_API_KEY` in host env
- Add timeouts/retries at call sites for production
- Rate-limit and log token usage if billing matters

### Pitfalls

- Hardcoded `sk-...` in source
- No handling for empty `message.content`
- Blocking calls in UI thread without timeout

---

## Module: M05 — Files and artifacts

### Purpose

Read inputs and persist API outputs (text, images, audio) predictably.

### When

Summaries from `.txt`, DALL·E downloads, TTS mp3, pipeline assets.

### Layout

```text
input/
output/
assets/images/
assets/audio/
```

### Code

```python
from pathlib import Path
import uuid

import requests


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def download_url(url: str, dest_dir: Path) -> Path:
    ensure_dir(dest_dir)
    out = dest_dir / f"{uuid.uuid4().hex}.png"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    out.write_bytes(resp.content)
    return out
```

### Run locally

```bash
pip install requests
python -c "from pathlib import Path; print(read_text(Path('text_to_summarize.txt')))"
```

### Deploy

- Mount persistent volume or object storage (S3, R2) for `output/`
- Do not rely on ephemeral container disk for user-facing assets

### Pitfalls

- Relative paths break when cwd changes → prefer `Path(__file__).resolve().parent`
- Huge files loaded entirely into memory

---

## Module: M06 — LangChain app

### Purpose

Composable prompts + model + parser chains (LCEL).

### When

Intro LangChain lessons, multi-step chains, Gradio backends.

### Layout

```text
langchain_basics.py
```

### Code

```python
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are concise."), ("user", "{topic}")]
)
model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
chain = prompt | model | StrOutputParser()


def run_chain(topic: str) -> str:
    return chain.invoke({"topic": topic})


if __name__ == "__main__":
    print(run_chain("quantum coffee"))
```

### Run locally

```bash
pip install langchain langchain-openai python-dotenv
python langchain_basics.py
```

### Deploy

- Keep chain build at import time or behind lazy init for faster cold starts
- Stream with `.stream()` for long outputs in UIs

### Pitfalls

- Missing `OPENAI_API_KEY` at import
- Mixing sync `invoke` inside async web handlers without offload

---

## Module: M07 — Gradio demo

### Purpose

Browser UI for quick prototypes and capstone demos.

### When

`gradio-story-and-image-demo` and similar “show the chain” apps.

### Layout

```text
gradio_project.py
generate_image.py    # optional import from sibling module
```

### Code

```python
import gradio as gr

from langchain_basics import run_chain  # your module


def ui_fn(topic: str) -> str:
    return run_chain(topic)


demo = gr.Blocks()
with demo:
    gr.Markdown("# Demo")
    topic = gr.Textbox(label="Topic")
    out = gr.Textbox(label="Output")
    btn = gr.Button("Run")
    btn.click(fn=ui_fn, inputs=topic, outputs=out)

if __name__ == "__main__":
    demo.launch()
```

### Run locally

```bash
pip install gradio
python gradio_project.py
# open printed local URL
```

### Deploy

- `demo.launch(server_name="0.0.0.0", server_port=7860)` behind reverse proxy
- Or use Gradio `share=True` only for temporary demos (not production)
- Container: expose port 7860, set auth if public

### Pitfalls

- Binding only to localhost on a remote server
- No auth on public Gradio endpoints

---

## Module: M08 — Streamlit app

### Purpose

Multi-widget web app for meme generator and internal tools.

### When

`streamlit-meme-app`, `automated-meme-generator`.

### Layout

```text
app.py
templates/
```

### Code

```python
import streamlit as st

st.set_page_config(page_title="Meme Gen", layout="wide")
st.title("Meme generator")

topic = st.text_input("Topic")
if st.button("Generate") and topic:
    with st.spinner("Working..."):
        # call meme_gpt / render_meme
        st.success(f"Done: {topic}")
```

### Run locally

```bash
pip install streamlit
streamlit run app.py
```

### Deploy

- Streamlit Community Cloud: connect repo, set secrets in UI
- Docker: `CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]`
- Set `OPENAI_API_KEY` in platform secrets

### Pitfalls

- Long blocking API calls freeze UI → use `st.spinner`, cache, or background jobs
- Secrets in `st.secrets` committed to repo

---

## Module: M09 — Batch / pipeline job

### Purpose

Orchestrate several steps (scrape → script → images → audio → video).

### When

Video capstone `main.py`, meme full pipeline.

### Layout

```text
main.py
assets/
screenshots/
output/
```

### Code

```python
from pathlib import Path


def step_scrape(out: Path) -> Path:
    # return path to screenshot
    return out / "page.png"


def step_script(image: Path) -> str:
    return "paragraph one\nparagraph two"


def step_render(script: str, work_dir: Path) -> Path:
    return work_dir / "final.mp4"


def main() -> None:
    work = Path("output")
    work.mkdir(exist_ok=True)
    img = step_scrape(work)
    script = step_script(img)
    video = step_render(script, work)
    print(f"wrote {video}")


if __name__ == "__main__":
    main()
```

### Run locally

```bash
python main.py
```

### Deploy

- Split into idempotent steps with checkpoints in `output/`
- Schedule via cron, GitHub Actions, or workflow engine
- Pass `--dry-run` (see M03) in CI without spending API credits

### Pitfalls

- One failure mid-pipeline loses all work → save intermediate artifacts
- Non-idempotent reruns duplicating charges

---

## Module: M10 — Dependencies

### Purpose

Reproducible installs across machines and deploy environments.

### When

Every project; before Docker build or CI.

### Layout

```text
requirements.txt
# optional for libraries you publish:
pyproject.toml
```

### Code

`requirements.txt` (lesson-sized app):

```text
openai>=1.40.0,<2
python-dotenv>=1.0.0,<2
requests>=2.31.0,<3
```

Pin exactly for production deploy:

```bash
pip freeze > requirements.lock.txt
```

### Run locally

```bash
pip install -r requirements.txt
pip list
```

### Deploy

- Install with `pip install -r requirements.txt` in Dockerfile or buildpack
- Pin versions to avoid surprise breaking releases
- Separate dev deps: `requirements-dev.txt` (pytest, ruff)

### Pitfalls

- Unpinned `langchain` / `moviepy` breaking on fresh install
- CUDA `torch` wheel mismatch on server vs laptop

---

## Module: M11 — Logging and errors

### Purpose

See what failed in cron, Docker, or cloud logs.

### When

Any script moving beyond interactive `print` debugging.

### Layout

```text
logging configured in main or config.py
```

### Code

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("app")


def safe_chat(client, user: str) -> str:
    try:
        # client call
        return "ok"
    except Exception:
        log.exception("chat failed for user prompt len=%s", len(user))
        raise
```

### Run locally

```bash
python main.py 2>&1 | tee run.log
```

### Deploy

- Log to stdout/stderr (12-factor); platform aggregates logs
- Never log secrets or full prompts if PII-sensitive

### Pitfalls

- Bare `except:` swallowing errors
- Only `print()` in production jobs

---

## Module: M12 — Config by environment

### Purpose

Switch behavior between development and production without code edits.

### When

Debug flags, mock APIs, different output paths, log levels.

### Layout

```text
.env              # APP_ENV=development
config.py
```

### Code

```python
import os

APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = APP_ENV == "development"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output" if DEBUG else "/var/app/output")
```

### Run locally

```bash
APP_ENV=development python main.py
APP_ENV=production OUTPUT_DIR=/tmp/out python main.py
```

### Deploy

- Set `APP_ENV=production` in host env
- Use platform secret manager for keys per environment

### Pitfalls

- `DEBUG=True` left on in production
- Development API keys used in prod billing account

---

## Module: M13 — Docker deploy

### Purpose

Package app + dependencies for consistent runs on any host.

### When

Shipping Gradio, Streamlit, or batch workers to a VPS or cloud.

### Layout

```text
Dockerfile
.dockerignore
requirements.txt
app.py
```

### Code

`Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit example:
ENV APP_ENV=production
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

`.dockerignore`:

```text
.venv
.env
__pycache__
output
.git
```

### Run locally

```bash
docker build -t my-app .
docker run --rm -p 8501:8501 -e OPENAI_API_KEY=sk-test my-app
```

### Deploy

- Push image to registry (GHCR, ECR)
- Run on Fly.io, Render, Cloud Run, ECS with env secrets injected
- Health check HTTP path if platform requires it

### Pitfalls

- Copying `.env` into image layers
- Image runs as root without need
- No `.dockerignore` → huge slow builds

---

## Module: M14 — Process managers

### Purpose

Keep apps running after SSH disconnect; restart on failure.

### When

VPS deploy of Streamlit/Gradio or long-running workers.

### Layout

```text
deploy/my-app.service   # systemd unit example
```

### Code

`my-app.service` (systemd):

```ini
[Unit]
Description=My Streamlit app
After=network.target

[Service]
User=deploy
WorkingDirectory=/opt/my-app
EnvironmentFile=/opt/my-app/.env
ExecStart=/opt/my-app/.venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Put nginx/Caddy in front for TLS on port 443.

### Run locally

Simulate: `nohup streamlit run app.py &` (prefer systemd in real deploy).

### Deploy

- systemd on VM
- Managed platforms (Render web service) hide this layer

### Pitfalls

- App listens on `127.0.0.1` but firewall expects public binding behind proxy only
- No restart policy → silent downtime

---

## Module: M15 — Pre-deploy checklist

### Purpose

Ship without leaking secrets or breaking installs.

### When

Before git push to public repo, Docker publish, or demo URL share.

### Layout

Use as a review list (no extra files required).

### Code

```text
[ ] .env in .gitignore; .env.example committed with placeholders
[ ] requirements.txt pinned or lockfile generated
[ ] python -m venv .venv && pip install -r requirements.txt on clean machine
[ ] APP_ENV=production tested once locally
[ ] No print() of API keys or user PII in logs
[ ] Entry command documented in README (streamlit run / python main.py)
[ ] Docker build succeeds without copying .env
[ ] Health: app starts, one happy-path request works
[ ] Rollback plan: previous image tag or git tag noted
```

### Run locally

Walk the checklist before `docker push` or `git push`.

### Deploy

Same checklist on staging before promoting to production.

### Pitfalls

- Skipping staging with real API keys
- No rollback → long outage on bad release

---

## Blank module template

Copy this block when you document a new pattern.

```markdown
## Module: Mxx — Title

### Purpose

### When

### Layout

```text

```

### Code

```python

```

### Run locally

```bash

```

### Deploy

### Pitfalls

```

---

## Quick map: Finxter module → cheatsheet modules

| Project module | Cheatsheet modules |
|----------------|-------------------|
| `api-keys-and-env` | M01, M02, M15 |
| `calling-an-api`, summarizer | M02, M04, M05 |
| DALL·E / TTS / Whisper | M04, M05, M10 |
| LangChain modules | M06, M04 |
| `gradio-story-and-image-demo` | M06, M07, M13 |
| `streamlit-meme-app` | M08, M13, M14 |
| `selenium-screenshot-scraper` | M03, M05, M11 |
| `automated-video-pipeline` | M09, M04, M05, M11 |
| `automated-meme-generator` | M08, M09, K recipes in projects README |

---

## Related docs

- Setup recipes and venv workflow: [`projects/README.md`](projects/README.md)
- PDF ↔ lesson artifacts: [`INDEX.md`](INDEX.md)
- Full chat example: [`projects/calling-an-api/README.md`](projects/calling-an-api/README.md)

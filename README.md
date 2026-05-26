# Applied AI Engineering

**Observable reference** for modular AI-engineering work: project **format**, runnable **application** patterns, and **deployment** usage (local demos, containers, checklists).

**Remote:** [github.com/obversarystudios/applied-ai-engineering](https://github.com/obversarystudios/applied-ai-engineering)  
**Narrative / research:** [obversarystudios.org](https://obversarystudios.org) · sibling eval layer: [observatory](https://github.com/obversarystudios/observatory)

Course structure follows [Finxter Academy](https://academy.finxter.com/) applied AI-engineering tracks. This repo is **not** a Finxter mirror; lesson PDFs are not included.

---

## Why this repo exists (observability)

Each module is a **traceable unit** you can revisit months later (or share with others):

| Layer | Where to look |
|-------|----------------|
| **Intent** | Module `README.md` — goal, layout, next steps |
| **Structure** | Suggested files, `requirements.txt`, `.gitignore`, [Modular file kit](projects/README.md#modular-file-kit) |
| **Application** | Reference `.py` scripts (growing module-by-module) |
| **Deployment** | [python_cheatsheet.md](python_cheatsheet.md) modules M01–M15 (venv, Gradio/Streamlit, Docker, ship checklist) |

Use this repository as the **public, sanitized** source of truth for format and usage. A private lab copy may also exist with PDFs and work-in-progress; neither replaces the other.

---

## Quick start

```bash
git clone https://github.com/obversarystudios/applied-ai-engineering.git
cd applied-ai-engineering
```

1. Open [INDEX.md](INDEX.md) — three tracks, lesson ↔ module map.  
2. Follow [projects/README.md](projects/README.md) — build order and setup recipes A–L.  
3. Per module:

```bash
cd projects/<module-name>
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# create .env with your API keys — never commit
python <entry_script>.py   # see module README
```

---

## Tracks and modules

| Track | Capstones | Atomic modules |
|-------|-----------|----------------|
| **Intro** (OpenAI, LangChain, Gradio, local, Gemini) | `gradio-story-and-image-demo` | `api-keys-and-env` … `google-gemini-multimodal` |
| **Video** (scrape → vision → DALL·E → TTS → MoviePy) | `automated-video-pipeline` | `selenium-screenshot-scraper` … `moviepy-video-assembly` |
| **Meme** (templates → GPT JSON → Pillow → Streamlit) | `automated-meme-generator` | `meme-template-loader` … `streamlit-meme-app` |

Full directory map: [INDEX.md — Modular projects map](INDEX.md#modular-projects-map).

---

## Honest scope (anti–overfitting)

**This repository does not claim:**

- Production readiness without explicit ops/runbook coverage  
- Generalization beyond the **modules and patterns** named here  
- Safety, fairness, or alignment guarantees without dedicated evaluation  
- Novelty in the literature — implementations follow public course and API docs  

**Evidence posture**

- **Verified here:** module READMEs, reference scripts where present, CI structure checks  
- **Described but not verified:** capstone orchestration until full code lands — treat as **roadmap**  

You supply your own API keys (`.env`, gitignored).

---

## Lab sync

From an Obversary lab tree, run [scripts/sync-to-github.sh](scripts/sync-to-github.sh) to **copy** (never delete) updates from `qi/education/ai-engineering-fliinxster/` into this staging layout before push.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Prefer one module or one track per PR.

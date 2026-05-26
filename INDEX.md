# Finxter AI Engineering — course index

**Public mirror (format, application, deployment):** [github.com/obversarystudios/applied-ai-engineering](https://github.com/obversarystudios/applied-ai-engineering)

Source: [Finxter Academy](https://academy.finxter.com/) PDF exports in this folder (17 lessons, 3 tracks).

Modular project stubs live in [`projects/`](projects/) — one directory per teachable unit or capstone.

---

## Track A — Intro to AI Engineering with Python (6 parts)

Broad survey course; cumulative project folder in the lessons is `Broad_intro_to_AI` / `Intro_to_AI_engineering`.

| Part | PDF | Topics | Key artifacts |
|------|-----|--------|----------------|
| 1/6 | `Intro to AI Engineering with Python (1_6) – ChatGPT and the OpenAI API – Finxter Academy.pdf` | OpenAI account, API keys, model pricing (`gpt-4o`, `gpt-4o-mini`), tokens | `.env`, `chat_gpt_request.py`, `text_to_summarize.txt` |
| 2/6 | `Intro to AI Engineering with Python (2_6) – Exploring Other AI APIs by OpenAI – Finxter Academy.pdf` | DALL·E 3, TTS, Whisper | `generate_image.py`, `generate_speech.py`, `transcribe_audio.py`, `output/`, `test_audio.mp3` |
| 3/6 | `Intro to AI Engineering with Python (3_6) – LangChain 101 – Finxter Academy.pdf` | LangChain LCEL, prompts, chains, invoke/stream/batch | `langchain_basics.py` |
| 4/6 | `Intro to AI Engineering with Python (4_6) – Rapid Prototyping and Demos Using Gradio – Finxter Academy.pdf` | Gradio Blocks UI; chains + DALL·E | `gradio_project.py` (“Silly-o-Matic”) |
| 5/6 | `Intro to AI Engineering with Python (5_6) – Local LLMs and HuggingFace 🤗 – Finxter Academy.pdf` | Ollama (`llama3`), Hugging Face Hub, Diffusers local image gen | CLI + `pip install diffusers transformers accelerate` (+ optional CUDA torch) |
| 6/6 | `Intro to AI Engineering with Python (6_6) – Google Gemini – Finxter Academy.pdf` | Gemini API, multimodal (image + text) | `simple_gemini_request.py`, `GOOGLE_API_KEY` in `.env` |

**Intro capstone (in-course):** `gradio-story-and-image-demo` — story + image description chains + Gradio (part 4).

---

## Track B — AI Meme Engineer (4 parts + intro)

End product: Streamlit app that generates 3 memes from a topic using templates + ChatGPT JSON + Pillow.

| Part | PDF | Topics | Key artifacts |
|------|-----|--------|----------------|
| 0/4 | `AI Meme Engineer (0_4) – Introduction – Finxter Academy.pdf` | Course map | — |
| 1/4 | `AI Meme Engineer (1_4) – Building a Fully Automated Meme Generator – Finxter Academy.pdf` | Project layout, `templates/`, `meme_data.json`, font metrics | `Meme_Gen/` structure, loader utilities |
| 2/4 | `AI Meme Engineer (2_4) – Calling ChatGPT and Generating Memes – Finxter Academy.pdf` | API key, system prompts, **JSON mode** | ChatGPT integration for meme text |
| 3/4 | `AI Meme Engineer (3_4) – Meme Image Generation – Finxter Academy.pdf` | Pillow text placement on templates | Image compositing functions |
| 4/4 | `AI Meme Engineer (4_4) – Meme Image Generation – Finxter Academy.pdf` | Wire pipeline + **Streamlit** UI | `app.py`, `streamlit run app.py` |

**Meme capstone:** `automated-meme-generator` — full `Meme_Gen` app.

---

## Track C — OpenAI Video Creator (6 parts)

End product: Topic in → script (GPT) → image prompts → DALL·E images → TTS → MoviePy video.

| Part | PDF | Topics | Key artifacts |
|------|-----|--------|----------------|
| 1/6 | `OpenAI Video Creator (1_6)_ Generating Video Ideas Using Web Scraping – Finxter Academy.pdf` | Selenium full-page screenshots, Pillow | `pillow`, `selenium` |
| 2/6 | `OpenAI Video Creator (2_6)_ Crafting Video Scripts with OpenAI's Image Processing Capabilities – Finxter Academy.pdf` | Vision API, base64 image encoding | `encode_image()`, chat with image content |
| 3/6 | `OpenAI Video Creator (3_6)_ OpenAI's Image Generation API – Finxter Academy.pdf` | DALL·E 3 generate + **variations** | `client.images.generate`, `create_variation` |
| 4/6 | `OpenAI Video Creator (4_6)_ OpenAI's Text-to-Speech – Finxter Academy.pdf` | TTS HD voices | `client.audio.speech.create`, `tts-1-hd` |
| 5/6 | `OpenAI Video Creator (5_6)_ Combining All Elements To Produce The Final Cut – Finxter Academy.pdf` | MoviePy: images + audio → video | `pip install moviepy` |
| 6/6 | `OpenAI Video Creator (6_6)_ Building a Fully Automated Video Creation System Using OpenAI & Python – Finxter Academy.pdf` | Full pipeline `main()` | `generate_paragraphs`, `generate_image_prompts`, `generate_image`, `generate_voiceover`, `create_video` |

**Video capstone:** `automated-video-pipeline` — parts 1–6 combined.

---

## Modular projects map

| Directory | Type | Source lesson(s) |
|-----------|------|------------------|
| [`projects/api-keys-and-env`](projects/api-keys-and-env/) | atomic | Intro 1/6 (pattern reused everywhere) |
| [`projects/calling-an-api`](projects/calling-an-api/) | atomic | Intro 1/6 |
| [`projects/chat-completions-summarizer`](projects/chat-completions-summarizer/) | atomic | Intro 1/6 |
| [`projects/dalle-image-generation`](projects/dalle-image-generation/) | atomic | Intro 2/6, Video 3/6 |
| [`projects/save-api-output-to-disk`](projects/save-api-output-to-disk/) | atomic | Intro 2/6 |
| [`projects/openai-text-to-speech`](projects/openai-text-to-speech/) | atomic | Intro 2/6, Video 4/6 |
| [`projects/openai-whisper-transcription`](projects/openai-whisper-transcription/) | atomic | Intro 2/6 |
| [`projects/langchain-prompts-and-chains`](projects/langchain-prompts-and-chains/) | atomic | Intro 3/6 |
| [`projects/langchain-multi-step-chain`](projects/langchain-multi-step-chain/) | atomic | Intro 3/6 |
| [`projects/gradio-story-and-image-demo`](projects/gradio-story-and-image-demo/) | capstone | Intro 4/6 |
| [`projects/ollama-local-llm`](projects/ollama-local-llm/) | atomic | Intro 5/6 |
| [`projects/huggingface-local-image-generation`](projects/huggingface-local-image-generation/) | atomic | Intro 5/6 |
| [`projects/google-gemini-multimodal`](projects/google-gemini-multimodal/) | atomic | Intro 6/6 |
| [`projects/selenium-screenshot-scraper`](projects/selenium-screenshot-scraper/) | atomic | Video 1/6 |
| [`projects/openai-vision-scriptwriter`](projects/openai-vision-scriptwriter/) | atomic | Video 2/6 |
| [`projects/moviepy-video-assembly`](projects/moviepy-video-assembly/) | atomic | Video 5/6 |
| [`projects/automated-video-pipeline`](projects/automated-video-pipeline/) | capstone | Video 1–6/6 |
| [`projects/meme-template-loader`](projects/meme-template-loader/) | atomic | Meme 1/4 |
| [`projects/chatgpt-json-meme-copy`](projects/chatgpt-json-meme-copy/) | atomic | Meme 2/4 |
| [`projects/pillow-meme-renderer`](projects/pillow-meme-renderer/) | atomic | Meme 3/4 |
| [`projects/streamlit-meme-app`](projects/streamlit-meme-app/) | atomic | Meme 4/4 |
| [`projects/automated-meme-generator`](projects/automated-meme-generator/) | capstone | Meme 0–4/4 |

See [`projects/README.md`](projects/README.md) for build order and shared dependencies. Applied Python patterns and deployment modules: [`python_cheatsheet.md`](python_cheatsheet.md). Vocabulary & ontology: [`../glossary/README.md`](../glossary/README.md).

# NewsFlow AI — Local Development Setup

## 1. Prerequisites

- **Python 3.10+** recommended. The pipeline is pure Python with no native extensions.
- **Node.js 18+** if you want to run the website locally (Vite + React).

## 2. Python Environment

```bash
# From repository root
python3 -m venv .venv            # Create virtual environment
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows PowerShell
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
# Installs: feedparser, requests, openai, python-dotenv
```

## 4. Environment Configuration

```bash
# The repo already has .env with OPENAI_API_KEY set.
# If you need to create one from the template:
cp .env.example .env            # Create .env from the example
# Then edit .env and add your actual key:
# OPENAI_API_KEY=sk-proj-...
```

**Verification**: Run `python -c "from ai.summarizer import API_KEY; print('OK')"` — it should not raise RuntimeError.

## 5. Run the Pipeline

```bash
python backend/main.py
```

**What happens** (5 steps, as documented in `AGENTS.md`):
1. Collect RSS news from BBC/DW feeds
2. Remove exact URL duplicates
3. Group similar stories (title similarity ≥ 0.82)
4. Send up to 15 articles to OpenAI for summarization (`gpt-5.6-luna`)
5. Save daily edition to `data/news_archive.json`

**Output**: Console output per step, plus `data/news_archive.json` updated atomically.

## 6. Run the Website (optional)

```bash
cd website
npm install          # Install React deps
npm run dev          # Start Vite dev server at http://localhost:3000
```

**Note**: The website currently has empty UI components (`App.js`, `index.js`, etc.). Running `npm run dev` will start a dev server but won't render meaningful content until pages/components are implemented.

## 7. Common Local Issues

- **`OPENAI_API_KEY` missing**: The summarizer raises `RuntimeError` at import. Ensure `.env` is loaded and the key is valid.
- **RSS feeds failing**: Network issues or feed downtime are handled gracefully (warnings printed, feed skipped).
- **Archive merge conflicts**: `data/news_archive.json` is atomically written via `.tmp` file swap. If you edit it manually, run the pipeline again to reconcile.
- **More than 15 articles**: Only the first 15 are sent to OpenAI per run. Re-run the pipeline for additional articles.
# NewsFlow AI — Agent Quickstart

## Pipeline flow (main entrypoint: `backend/main.py`)

1. **Collect RSS** (`collector/rss.py`) — pulls articles from 5 categories across BBC and DW feeds.
2. **Exact deduplication** (`backend/utils/deduplicate.py`) — removes articles with identical normalized URLs.
3. **Similar story detection** (`backend/utils/deduplicate.py:find_similar_articles`) — groups articles with title similarity >= 0.82 (default threshold).
4. **OpenAI summarization** (`backend/ai/processor.py`) — sends up to 15 articles per run to `gpt-5.6-luna` via OpenAI Responses API; each article gets summary, key_points, keywords, category, importance.
5. **Save archive** (`backend/storage/archive.py`) — persists daily edition to `data/news_archive.json`, merging with existing entries and avoiding duplicate article IDs.

**Command:** `python backend/main.py`

## Environment

- **Required**: `OPENAI_API_KEY` must be set in `.env` at repo root (see `.env` example).
- **Python deps**: `feedparser`, `requests`, `openai`, `python-dotenv` (see `requirements.txt`).
- The summarizer (`backend/ai/summarizer.py`) loads `.env` via `load_dotenv()` and will raise `RuntimeError` if `OPENAI_API_KEY` is missing.

## Key conventions & quirks

- **Model name**: `gpt-5.6-luna` in `summarizer.py` — appears to be a non-standard/placeholder name. Verify availability before running.
- **Max articles per run**: `MAX_ARTICLES_PER_RUN = 15` in `backend/ai/processor.py` — only the first 15 articles are sent to OpenAI.
- **Deduplication threshold**: `threshold=0.82` in `find_similar_articles()` — adjust if similar-story grouping seems off.
- **Archive path**: `data/news_archive.json` — relative to repo root; atomically written via `.tmp` file swap.
- **Category mapping**: Articles inherit category from their RSS feed key (`world`, `technology`, `business`, `science`).
- **Article ID**: Stable SHA-256 hash of the original URL (first 16 hex chars), generated in `rss.py:generate_article_id()`.

## Common agent mistakes to avoid

- **Forgetting `.env`**: The pipeline will crash at import if `OPENAI_API_KEY` is unset.
- **Running without collecting first**: `main.py` expects articles from `collect_news()`; running steps out of order will lose data.
- **Assuming all 15 articles are sent**: If OpenAI calls fail, fewer articles may be processed — the pipeline handles this gracefully but output counts will differ.
- **Ignoring the `.tmp` archive write**: `save_archive()` writes to a temporary file then replaces the original — never edit `news_archive.json` manually while a run is in progress.

## Repository structure

```
backend/         # Python pipeline package
  ai/            # OpenAI summarization
  collector/     # RSS feed collection
  storage/       # Archive persistence
  utils/         # Deduplication helpers
  main.py        # Orchestrates the full pipeline
data/            # news_archive.json (generated)
website/         # Frontend (React, currently empty — separate from pipeline)
.github/workflows/news.yml  # CI workflow (currently empty)
.env             # OPENAI_API_KEY (gitignored)
requirements.txt  # Python dependencies
README.md        # Project overview (empty)
```
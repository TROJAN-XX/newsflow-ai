"""
NewsFlow AI — Centralized Configuration

All tunable settings live here. Values are read from
environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ── OpenAI ─────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

# ── Pipeline ───────────────────────────────────────────
MAX_ARTICLES_PER_RUN = int(
    os.getenv("MAX_ARTICLES_PER_RUN", "20")
)

SIMILARITY_THRESHOLD = float(
    os.getenv("SIMILARITY_THRESHOLD", "0.82")
)

# ── Archive ────────────────────────────────────────────
ARCHIVE_DIR = os.getenv("ARCHIVE_DIR", "data")
ARCHIVE_FILENAME = "news_archive.json"

# ── Website sync ───────────────────────────────────────
WEBSITE_DATA_DIR = os.path.join(
    "website", "public", "data"
)

# ── Request settings ───────────────────────────────────
REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "15")
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "2")
)

"""
NewsFlow AI — Archive Storage

Manages the JSON archive of daily news editions.
Uses atomic writes to prevent corruption.
"""

import json
import os
from datetime import datetime, timezone

from backend.utils.config import (
    ARCHIVE_DIR,
    ARCHIVE_FILENAME
)


ARCHIVE_FILE = os.path.join(
    ARCHIVE_DIR,
    ARCHIVE_FILENAME
)


def load_archive():

    if not os.path.exists(ARCHIVE_FILE):
        return {}

    try:

        with open(
            ARCHIVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}


def save_archive(archive):

    os.makedirs(
        os.path.dirname(ARCHIVE_FILE)
        or ".",
        exist_ok=True
    )

    temporary_file = (
        ARCHIVE_FILE + ".tmp"
    )

    with open(
        temporary_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            archive,
            file,
            indent=2,
            ensure_ascii=False
        )

    os.replace(
        temporary_file,
        ARCHIVE_FILE
    )


def save_daily_news(
    articles,
    articles_collected=0,
    duplicates_removed=0,
    daily_digest=None
):

    archive = load_archive()

    today = datetime.now(
        timezone.utc
    ).date().isoformat()

    existing_edition = archive.get(
        today,
        {}
    )

    existing_articles = {
        article.get("id"): article
        for article in existing_edition.get(
            "articles",
            []
        )
        if article.get("id")
    }

    # Update existing articles or add new ones.
    for article in articles:

        article_id = article.get("id")

        if not article_id:
            continue

        existing_articles[article_id] = article

    final_articles = list(
        existing_articles.values()
    )

    # Newest articles first.
    final_articles.sort(
        key=lambda article: (
            article.get("published_at")
            or ""
        ),
        reverse=True
    )

    categories = {}

    for article in final_articles:

        category = article.get(
            "category",
            "other"
        )

        categories[category] = (
            categories.get(category, 0)
            + 1
        )

    # Count AI-processed articles
    ai_processed = sum(
        1 for article in final_articles
        if article.get("ai", {}).get("processed", False)
    )

    edition = {

        "date": today,

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "statistics": {

            "articles_collected":
                articles_collected,

            "duplicates_removed":
                duplicates_removed,

            "total_articles":
                len(final_articles),

            "ai_processed":
                ai_processed
        },

        "categories": categories,

        "daily_digest": (
            daily_digest
            if daily_digest is not None
            else existing_edition.get(
                "daily_digest"
            )
        ),

        "articles": final_articles
    }

    archive[today] = edition

    save_archive(archive)

    return edition
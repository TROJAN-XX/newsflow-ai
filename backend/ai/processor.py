"""
NewsFlow AI — Article Processor

Selects and processes articles through the AI summarizer
in batches with progress reporting.
"""

import time
from .summarizer import summarize_article

from backend.utils.config import MAX_ARTICLES_PER_RUN


def process_articles(articles):

    processed = []

    # Sort by importance hints (category diversity)
    # then take the configured maximum
    selected_articles = articles[:MAX_ARTICLES_PER_RUN]

    total = len(selected_articles)

    print(
        f"  Sending {total} articles to AI...\n"
    )

    succeeded = 0
    failed = 0

    for index, article in enumerate(
        selected_articles,
        start=1
    ):

        title = article["title"]
        short_title = (
            title[:60] + "..."
            if len(title) > 60
            else title
        )

        print(
            f"  [{index}/{total}] "
            f"{short_title}"
        )

        try:

            ai_result = summarize_article(article)

            article["ai"] = ai_result

            processed.append(article)

            succeeded += 1

            # Small delay to respect rate limits
            if index < total:
                time.sleep(0.5)

        except Exception as error:

            print(
                f"    ✗ AI failed: {error}"
            )

            article["ai"] = {
                "summary": None,
                "key_points": [],
                "keywords": [],
                "category": article.get(
                    "category",
                    "other"
                ),
                "importance": None,
                "processed": False,
                "error": str(error)
            }

            processed.append(article)

            failed += 1

    print(
        f"\n  AI results: {succeeded} ok, "
        f"{failed} failed"
    )

    return processed
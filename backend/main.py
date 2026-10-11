"""
NewsFlow AI — Main Pipeline

Orchestrates the full news processing pipeline:
1. Collect RSS feeds
2. Remove exact duplicates
3. Detect similar stories
4. Generate AI summaries
5. Create daily digest
6. Save to archive
"""

import sys
import time
from datetime import datetime, timedelta, timezone

from backend.collector.rss import collect_news

from backend.storage.archive import save_daily_news

from backend.utils.deduplicate import (
    deduplicate_articles,
    find_similar_articles
)

from backend.ai.processor import process_articles

from backend.ai.digest import generate_daily_digest

IST = timezone(timedelta(hours=5, minutes=30), name="IST")


def main():

    start_time = time.time()

    today = datetime.now(
        IST
    ).strftime("%A, %B %d, %Y")

    print()
    print("=" * 60)
    print("  NEWSFLOW AI")
    print("  AI-Powered News Intelligence Pipeline")
    print(f"  {today}")
    print("=" * 60)

    # --------------------------------------------------
    # 1. COLLECT
    # --------------------------------------------------

    print(
        "\n▸ [1/6] Collecting RSS feeds...\n"
    )

    articles = collect_news()

    collected_count = len(
        articles
    )

    print(
        f"\n  Total collected: {collected_count}"
    )

    if not articles:

        print(
            "\n  ✗ No articles found. Exiting."
        )

        return

    # --------------------------------------------------
    # 2. EXACT DEDUPLICATION
    # --------------------------------------------------

    print(
        "\n▸ [2/6] Removing exact duplicates..."
    )

    (
        unique_articles,
        duplicate_count
    ) = deduplicate_articles(
        articles
    )

    print(
        f"  Duplicates removed: "
        f"{duplicate_count}"
    )

    print(
        f"  Unique articles: "
        f"{len(unique_articles)}"
    )

    # --------------------------------------------------
    # 3. SIMILAR STORIES
    # --------------------------------------------------

    print(
        "\n▸ [3/6] Detecting similar stories..."
    )

    similar_groups = (
        find_similar_articles(
            unique_articles
        )
    )

    similar_count = sum(
        len(group) - 1
        for group in similar_groups
    )

    print(
        f"  Story clusters: "
        f"{len(similar_groups)}"
    )

    print(
        f"  Related articles: "
        f"{similar_count}"
    )

    # --------------------------------------------------
    # 4. AI PROCESSING
    # --------------------------------------------------

    print(
        "\n▸ [4/6] Generating AI summaries...\n"
    )

    processed_articles = (
        process_articles(
            unique_articles
        )
    )

    ai_count = sum(
        1 for a in processed_articles
        if a.get("ai", {}).get("processed", False)
    )

    print(
        f"\n  AI summaries: {ai_count}"
        f"/{len(processed_articles)}"
    )

    # --------------------------------------------------
    # 5. DAILY DIGEST
    # --------------------------------------------------

    print(
        "\n▸ [5/6] Generating daily digest..."
    )

    daily_digest = (
        generate_daily_digest(
            processed_articles
        )
    )

    print(
        "  ✓ Daily digest generated"
    )

    # --------------------------------------------------
    # 6. ARCHIVE
    # --------------------------------------------------

    print(
        "\n▸ [6/6] Saving daily archive..."
    )

    daily_news = save_daily_news(

        processed_articles,

        articles_collected=
            collected_count,

        duplicates_removed=
            duplicate_count,

        daily_digest=
            daily_digest
    )

    print(
        "  ✓ Archive saved"
    )

    # --------------------------------------------------
    # REPORT
    # --------------------------------------------------

    elapsed = round(
        time.time() - start_time, 1
    )

    print()
    print("=" * 60)
    print("  TODAY'S EDITION")
    print("=" * 60)

    print(
        f"  Date:       "
        f"{daily_news['date']}"
    )

    stats = daily_news["statistics"]

    print(
        f"  Collected:  "
        f"{stats['articles_collected']}"
    )

    print(
        f"  Duplicates: "
        f"{stats['duplicates_removed']}"
    )

    print(
        f"  Stored:     "
        f"{stats['total_articles']}"
    )

    print(
        f"  AI done:    "
        f"{stats.get('ai_processed', '—')}"
    )

    print(
        "\n  Categories:"
    )

    for (
        category,
        count
    ) in daily_news[
        "categories"
    ].items():

        print(
            f"    {category}: {count}"
        )

    if daily_digest:
        print(
            f"\n  Headline: "
            f"{daily_digest.get('headline', '—')}"
        )

    print(
        f"\n  Pipeline completed in "
        f"{elapsed}s"
    )

    print(
        "\n  NewsFlow AI ✓\n"
    )


if __name__ == "__main__":
    main()
from collector.rss import collect_news

from storage.archive import save_daily_news

from utils.deduplicate import (
    deduplicate_articles,
    find_similar_articles
)

from ai.processor import process_articles


def main():

    print("=" * 60)
    print("NEWSFLOW AI")
    print("AI News Pipeline")
    print("=" * 60)

    # --------------------------------------------------
    # 1. COLLECT
    # --------------------------------------------------

    print("\n[1/5] Collecting RSS news...\n")

    articles = collect_news()

    collected_count = len(articles)

    print(
        f"\nCollected: {collected_count}"
    )

    if not articles:

        print("No articles found.")

        return

    # --------------------------------------------------
    # 2. DEDUPLICATE
    # --------------------------------------------------

    print(
        "\n[2/5] Removing exact duplicates..."
    )

    (
        unique_articles,
        duplicate_count
    ) = deduplicate_articles(
        articles
    )

    print(
        f"Duplicates removed: "
        f"{duplicate_count}"
    )

    print(
        f"Unique articles: "
        f"{len(unique_articles)}"
    )

    # --------------------------------------------------
    # 3. FIND SIMILAR STORIES
    # --------------------------------------------------

    print(
        "\n[3/5] Detecting similar stories..."
    )

    similar_groups = find_similar_articles(
        unique_articles
    )

    print(
        f"Potential story groups: "
        f"{len(similar_groups)}"
    )

    # --------------------------------------------------
    # 4. AI PROCESSING
    # --------------------------------------------------

    print(
        "\n[4/5] Processing articles with AI..."
    )

    processed_articles = process_articles(
        unique_articles
    )

    print(
        f"\nAI processed: "
        f"{len(processed_articles)}"
    )

    # --------------------------------------------------
    # 5. SAVE
    # --------------------------------------------------

    print(
        "\n[5/5] Saving archive..."
    )

    daily_news = save_daily_news(

        processed_articles,

        articles_collected=
            collected_count,

        duplicates_removed=
            duplicate_count
    )

    print("\n" + "=" * 60)

    print("TODAY'S EDITION")

    print("=" * 60)

    print(
        f"Date: "
        f"{daily_news['date']}"
    )

    print(
        f"Collected: "
        f"{daily_news['statistics']['articles_collected']}"
    )

    print(
        f"Duplicates: "
        f"{daily_news['statistics']['duplicates_removed']}"
    )

    print(
        f"Published: "
        f"{daily_news['statistics']['total_articles']}"
    )

    print("\nCategories:")

    for category, count in (
        daily_news["categories"].items()
    ):

        print(
            f"  {category}: {count}"
        )

    print("\nNewsFlow AI completed.")


if __name__ == "__main__":
    main()
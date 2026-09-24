from collector.rss import collect_news
from storage.archive import save_daily_news


def main():

    print("=" * 60)
    print("NEWSFLOW AI")
    print("RSS News Collector")
    print("=" * 60)

    print("\nCollecting news...\n")

    articles = collect_news()

    print(
        f"\nCollected {len(articles)} articles."
    )

    if not articles:

        print("No articles found.")
        return

    print("\nSaving today's archive...")

    daily_news = save_daily_news(
        articles
    )

    print("\nToday's edition:")
    print(
        f"Date: {daily_news['date']}"
    )

    print(
        f"Total articles: "
        f"{daily_news['statistics']['total_articles']}"
    )

    print("\nCategories:")

    for category, count in (
        daily_news["categories"].items()
    ):

        print(
            f"  {category}: {count}"
        )

    print("\nDone!")


if __name__ == "__main__":
    main()
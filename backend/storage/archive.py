import json
from pathlib import Path
from datetime import datetime, timezone


ARCHIVE_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "news_archive.json"
)


def load_archive():

    if not ARCHIVE_FILE.exists():
        return {}

    try:

        with open(
            ARCHIVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError:

        print("Warning: Archive JSON is invalid.")

        return {}


def save_archive(archive):

    ARCHIVE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary_file = ARCHIVE_FILE.with_suffix(".tmp")

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

    temporary_file.replace(ARCHIVE_FILE)

def save_daily_news(
    articles,
    articles_collected=None,
    duplicates_removed=0
):

    archive = load_archive()

    today = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d")

    existing_articles = (
        archive
        .get(today, {})
        .get("articles", [])
    )

    existing_ids = {
        article["id"]
        for article in existing_articles
    }

    new_articles = []

    for article in articles:

        if article["id"] not in existing_ids:

            new_articles.append(
                article
            )

            existing_ids.add(
                article["id"]
            )

    combined_articles = (
        existing_articles +
        new_articles
    )

    category_counts = {}

    for article in combined_articles:

        category = article.get(
            "category",
            "uncategorized"
        )

        category_counts[category] = (
            category_counts.get(
                category,
                0
            ) + 1
        )

    archive[today] = {

        "date": today,

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "statistics": {

            "articles_collected":
                articles_collected
                if articles_collected is not None
                else len(articles),

            "duplicates_removed":
                duplicates_removed,

            "articles_added":
                len(new_articles),

            "total_articles":
                len(combined_articles)
        },

        "categories": category_counts,

        "articles": combined_articles
    }

    save_archive(archive)

    return archive[today]

    archive = load_archive()

    today = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d")

    existing_articles = (
        archive
        .get(today, {})
        .get("articles", [])
    )

    existing_ids = {
        article["id"]
        for article in existing_articles
    }

    new_articles = []

    for article in articles:

        if article["id"] not in existing_ids:

            new_articles.append(article)

            existing_ids.add(article["id"])

    combined_articles = (
        existing_articles +
        new_articles
    )

    category_counts = {}

    for article in combined_articles:

        category = article.get(
            "category",
            "uncategorized"
        )

        category_counts[category] = (
            category_counts.get(category, 0) + 1
        )

    archive[today] = {

        "date": today,

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "statistics": {

            "articles_collected":
                len(articles),

            "articles_added":
                len(new_articles),

            "total_articles":
                len(combined_articles)
        },

        "categories": category_counts,

        "articles": combined_articles
    }

    save_archive(archive)

    return archive[today]
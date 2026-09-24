import feedparser
from datetime import datetime, timezone
from hashlib import sha256


RSS_FEEDS = {
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ],

    "technology": [
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
    ],

    "business": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
    ],

    "science": [
        "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    ],
}


def generate_article_id(url):
    """
    Generate a stable ID from the original article URL.
    """

    return sha256(
        url.encode("utf-8")
    ).hexdigest()[:16]


def parse_date(entry):
    """
    Convert RSS publication date into ISO format.
    """

    if hasattr(entry, "published_parsed") and entry.published_parsed:

        dt = datetime(
            *entry.published_parsed[:6],
            tzinfo=timezone.utc
        )

        return dt.isoformat()

    return None


def clean_article(entry, category, feed_url):
    """
    Convert an RSS entry into our standard article structure.
    """

    title = entry.get("title", "").strip()

    description = (
        entry.get("summary")
        or entry.get("description")
        or ""
    ).strip()

    url = entry.get("link", "").strip()

    if not title or not url:
        return None

    article = {
        "id": generate_article_id(url),

        "title": title,

        "description": description,

        "source": {
            "name": "BBC News",
            "feed_url": feed_url
        },

        "original_url": url,

        "published_at": parse_date(entry),

        "category": category,

        "author": entry.get("author"),

        "image_url": None,

        "ai": {
            "summary": None,
            "key_points": [],
            "keywords": []
        }
    }

    return article


def collect_news():

    articles = []

    for category, feeds in RSS_FEEDS.items():

        for feed_url in feeds:

            print(f"Fetching: {feed_url}")

            feed = feedparser.parse(feed_url)

            if feed.bozo:
                print(f"Warning: Could not completely parse {feed_url}")

            for entry in feed.entries:

                article = clean_article(
                    entry,
                    category,
                    feed_url
                )

                if article:
                    articles.append(article)

    return articles
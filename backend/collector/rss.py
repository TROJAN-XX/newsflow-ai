import feedparser
import hashlib
import re
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

from html import unescape

from backend.utils.config import (
    REQUEST_TIMEOUT,
    MAX_RETRIES
)


RSS_FEEDS = {
    "world": [
        {
            "name": "BBC News",
            "url": "https://feeds.bbci.co.uk/news/world/rss.xml"
        },
        {
            "name": "DW",
            "url": "https://rss.dw.com/xml/rss-en-world"
        },
        {
            "name": "Al Jazeera",
            "url": "https://www.aljazeera.com/xml/rss/all.xml"
        },
        {
            "name": "Reuters World",
            "url": "https://feeds.reuters.com/Reuters/worldNews"
        }
    ],

    "technology": [
        {
            "name": "BBC Technology",
            "url": "https://feeds.bbci.co.uk/news/technology/rss.xml"
        },
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed/"
        },
        {
            "name": "Ars Technica",
            "url": "https://feeds.arstechnica.com/arstechnica/index"
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com/rss/index.xml"
        }
    ],

    "business": [
        {
            "name": "BBC Business",
            "url": "https://feeds.bbci.co.uk/news/business/rss.xml"
        },
        {
            "name": "CNBC",
            "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"
        }
    ],

    "science": [
        {
            "name": "BBC Science",
            "url": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
        },
        {
            "name": "Phys.org",
            "url": "https://phys.org/rss-feed/"
        },
        {
            "name": "Space.com",
            "url": "https://www.space.com/feeds/all"
        }
    ],

    "health": [
        {
            "name": "BBC Health",
            "url": "https://feeds.bbci.co.uk/news/health/rss.xml"
        },
        {
            "name": "Medical News Today",
            "url": "https://www.medicalnewstoday.com/newsrss"
        }
    ],

    "sports": [
        {
            "name": "BBC Sport",
            "url": "https://feeds.bbci.co.uk/sport/rss.xml"
        },
        {
            "name": "ESPN",
            "url": "https://www.espn.com/espn/rss/news"
        }
    ],

    "entertainment": [
        {
            "name": "BBC Entertainment",
            "url": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml"
        }
    ]
}


def generate_article_id(url):
    """
    Generate a stable ID from the article URL.
    """

    normalized_url = url.strip().lower()

    return hashlib.sha256(
        normalized_url.encode("utf-8")
    ).hexdigest()[:16]


def clean_text(text):
    """
    Remove HTML and unnecessary whitespace.
    """

    if not text:
        return ""

    text = unescape(text)

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def parse_date(entry):
    """
    Convert RSS publication date to ISO format.
    """

    if (
        hasattr(entry, "published_parsed")
        and entry.published_parsed
    ):

        dt = datetime(
            *entry.published_parsed[:6],
            tzinfo=timezone.utc
        )

        return dt.isoformat()

    if (
        hasattr(entry, "updated_parsed")
        and entry.updated_parsed
    ):

        dt = datetime(
            *entry.updated_parsed[:6],
            tzinfo=timezone.utc
        )

        return dt.isoformat()

    return None


def extract_image(entry):
    """
    Try different RSS formats to find an article image.
    """

    # media:content
    media_content = entry.get("media_content")

    if media_content:

        for media in media_content:

            url = media.get("url")

            if url:
                return url

    # media:thumbnail
    media_thumbnail = entry.get("media_thumbnail")

    if media_thumbnail:

        for media in media_thumbnail:

            url = media.get("url")

            if url:
                return url

    # enclosure
    enclosures = entry.get("enclosures")

    if enclosures:

        for enclosure in enclosures:

            url = enclosure.get("href")

            if url:
                return url

            url = enclosure.get("url")

            if url:
                return url

    # image inside description
    description = (
        entry.get("summary")
        or entry.get("description")
        or ""
    )

    image_match = re.search(
        r'<img[^>]+src=["\']([^"\']+)["\']',
        description,
        re.IGNORECASE
    )

    if image_match:
        return image_match.group(1)

    return None


def extract_author(entry):
    """
    Extract author using common RSS fields.
    """

    author = entry.get("author")

    if author:
        return clean_text(author)

    authors = entry.get("authors")

    if authors:

        names = []

        for item in authors:

            name = item.get("name")

            if name:
                names.append(
                    clean_text(name)
                )

        if names:
            return ", ".join(names)

    return None


def clean_article(
    entry,
    category,
    source_name,
    feed_url
):

    title = clean_text(
        entry.get("title", "")
    )

    description = clean_text(
        entry.get("summary")
        or entry.get("description")
        or ""
    )

    url = entry.get(
        "link",
        ""
    ).strip()

    if not title or not url:
        return None

    parsed_url = urlparse(url)

    domain = parsed_url.netloc

    article = {

        "id": generate_article_id(url),

        "title": title,

        "description": description,

        "source": {

            "name": source_name,

            "domain": domain,

            "feed_url": feed_url
        },

        "original_url": url,

        "published_at": parse_date(entry),

        "category": category,

        "author": extract_author(entry),

        "image_url": extract_image(entry),

        "ai": {
            "summary": None,
            "key_points": [],
            "keywords": [],
            "category": category,
            "importance": None,
            "processed": False,
            "error": None
        }
    }

    return article


def fetch_feed_with_retry(feed_url, source_name):
    """
    Fetch an RSS feed with retry logic and timeout.
    """

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            feed = feedparser.parse(feed_url)

            if feed.bozo and not feed.entries:

                if attempt < MAX_RETRIES:
                    print(
                        f"  Retry {attempt}/{MAX_RETRIES} "
                        f"for {source_name}..."
                    )
                    time.sleep(2 * attempt)
                    continue

            return feed

        except Exception as error:

            if attempt < MAX_RETRIES:
                print(
                    f"  Retry {attempt}/{MAX_RETRIES} "
                    f"for {source_name}: {error}"
                )
                time.sleep(2 * attempt)
            else:
                raise

    return None


def collect_news():

    articles = []

    total_sources = sum(
        len(sources)
        for sources in RSS_FEEDS.values()
    )

    fetched = 0
    failed = 0

    for category, sources in RSS_FEEDS.items():

        for source in sources:

            source_name = source["name"]

            feed_url = source["url"]

            print(
                f"  [{fetched + failed + 1}"
                f"/{total_sources}] "
                f"{source_name}..."
            )

            try:

                feed = fetch_feed_with_retry(
                    feed_url,
                    source_name
                )

                if feed is None:
                    failed += 1
                    continue

                if feed.bozo and feed.entries:
                    print(
                        f"  ⚠ Partial parse: "
                        f"{source_name}"
                    )

                source_count = 0

                for entry in feed.entries:

                    article = clean_article(
                        entry,
                        category,
                        source_name,
                        feed_url
                    )

                    if article:

                        articles.append(
                            article
                        )

                        source_count += 1

                print(
                    f"    ✓ {source_count} articles"
                )

                fetched += 1

            except Exception as error:

                print(
                    f"    ✗ Failed: {error}"
                )

                failed += 1

    print(
        f"\n  Sources: {fetched} ok, "
        f"{failed} failed"
    )

    return articles
import re
from difflib import SequenceMatcher
from urllib.parse import urlparse


def normalize_title(title):
    """
    Normalize a title for comparison.
    """

    title = title.lower()

    title = re.sub(
        r"[^a-z0-9\s]",
        "",
        title
    )

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    return title.strip()


def title_similarity(title_a, title_b):

    a = normalize_title(title_a)
    b = normalize_title(title_b)

    return SequenceMatcher(
        None,
        a,
        b
    ).ratio()


def normalize_url(url):

    parsed = urlparse(url)

    return (
        parsed.netloc.lower(),
        parsed.path.rstrip("/").lower()
    )


def deduplicate_articles(articles):

    unique_articles = []

    seen_urls = set()

    duplicate_count = 0

    for article in articles:

        url_key = normalize_url(
            article["original_url"]
        )

        # Exact URL duplicate
        if url_key in seen_urls:

            duplicate_count += 1

            continue

        seen_urls.add(url_key)

        unique_articles.append(
            article
        )

    return (
        unique_articles,
        duplicate_count
    )


def find_similar_articles(
    articles,
    threshold=0.82
):

    groups = []

    processed = set()

    for i, article in enumerate(articles):

        if i in processed:
            continue

        group = [article]

        processed.add(i)

        for j in range(
            i + 1,
            len(articles)
        ):

            if j in processed:
                continue

            similarity = title_similarity(
                article["title"],
                articles[j]["title"]
            )

            if similarity >= threshold:

                group.append(
                    articles[j]
                )

                processed.add(j)

        if len(group) > 1:

            groups.append(group)

    return groups
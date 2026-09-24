from .summarizer import summarize_article


MAX_ARTICLES_PER_RUN = 15


def process_articles(articles):

    processed = []

    selected_articles = articles[
        :MAX_ARTICLES_PER_RUN
    ]

    print(
        f"Sending {len(selected_articles)} "
        f"articles to OpenAI..."
    )

    for index, article in enumerate(
        selected_articles,
        start=1
    ):

        print(
            f"[{index}/{len(selected_articles)}] "
            f"{article['title']}"
        )

        try:

            ai_result = summarize_article(
                article
            )

            article["ai"] = ai_result

            processed.append(
                article
            )

        except Exception as error:

            print(
                f"AI processing failed: {error}"
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
                "error": str(error)
            }

            processed.append(
                article
            )

    return processed
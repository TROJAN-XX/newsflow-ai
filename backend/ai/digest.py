"""
NewsFlow AI — Daily Digest Generator

Uses OpenAI to produce a structured daily news digest
from AI-processed articles.
"""

import json
from datetime import datetime, timezone

from .summarizer import client, MODEL


DIGEST_SYSTEM_PROMPT = """
You are the editor of NewsFlow AI.

Create a concise daily news digest from the
AI-processed articles provided to you.

RULES:

1. Use ONLY information contained in the supplied articles.
2. Do not invent facts.
3. Do not add outside knowledge.
4. Keep the writing factual and neutral.
5. Do not copy article text verbatim.
6. Preserve uncertainty when sources are uncertain.
7. Political stories must be described neutrally.
8. Never endorse or oppose political candidates,
   parties, policies or viewpoints.
9. Do not rank political actors.
10. Keep the digest concise.
11. Return ONLY valid JSON.
"""


def generate_daily_digest(articles):

    if not articles:
        return {
            "headline": "Today's News in Brief",
            "intro": "No articles were available.",
            "top_stories": [],
            "sections": {}
        }

    article_data = []

    for article in articles:

        ai = article.get("ai", {})

        article_data.append({
            "id": article.get("id"),
            "title": article.get("title"),
            "source": article.get(
                "source",
                {}
            ).get(
                "name",
                "Unknown"
            ),
            "category": article.get(
                "category",
                "other"
            ),
            "summary": ai.get(
                "summary"
            ),
            "key_points": ai.get(
                "key_points",
                []
            ),
            "importance": ai.get(
                "importance"
            )
        })

    prompt = f"""
Create today's NewsFlow AI daily digest.

ARTICLES:

{json.dumps(
    article_data,
    indent=2,
    ensure_ascii=False
)}

Return EXACTLY this JSON structure:

{{
    "headline": "Today's News in Brief",
    "intro": "A concise overview of today's major developments.",
    "top_stories": [
        "article-id-1",
        "article-id-2",
        "article-id-3"
    ],
    "sections": {{
        "technology": "Short overview...",
        "business": "Short overview...",
        "world": "Short overview...",
        "science": "Short overview...",
        "other": "Short overview..."
    }}
}}

IMPORTANT:

- top_stories must contain IDs from the supplied articles.
- Select up to 3 top stories.
- Only include categories that actually exist.
- Keep each section concise.
- Do not invent information.
"""

    response = client.responses.create(
        model=MODEL,
        instructions=DIGEST_SYSTEM_PROMPT,
        input=prompt
    )

    raw_output = response.output_text.strip()

    # Handle markdown-wrapped JSON responses
    if raw_output.startswith("```"):
        lines = raw_output.split("\n")
        lines = [
            line for line in lines
            if not line.strip().startswith("```")
        ]
        raw_output = "\n".join(lines).strip()

    try:

        digest = json.loads(
            raw_output
        )

    except json.JSONDecodeError:

        raise ValueError(
            "OpenAI returned invalid digest JSON:\n"
            + raw_output
        )

    valid_ids = {
        article["id"]
        for article in articles
    }

    digest["top_stories"] = [
        article_id
        for article_id in digest.get(
            "top_stories",
            []
        )
        if article_id in valid_ids
    ][:3]

    digest["generated_at"] = (
        datetime.now(timezone.utc)
        .isoformat()
    )

    digest["model"] = MODEL

    return digest
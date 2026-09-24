import json
import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not configured."
    )


client = OpenAI(
    api_key=API_KEY
)


MODEL = "gpt-5.6-luna"


SYSTEM_PROMPT = """
You are an AI news editor.

Your job is to analyze news articles and produce concise,
factual and neutral summaries.

IMPORTANT RULES:

1. Do not invent facts.
2. Only use information provided in the article.
3. Preserve uncertainty when the article is uncertain.
4. Do not present speculation as fact.
5. Do not add information from your own knowledge.
6. Do not copy the article verbatim.
7. Keep summaries concise.
8. Preserve important names, dates, numbers and locations.
9. The original source URL must never be modified.
10. Return ONLY valid JSON.
"""


def summarize_article(article):

    title = article.get(
        "title",
        ""
    )

    description = article.get(
        "description",
        ""
    )

    source = article.get(
        "source",
        {}
    ).get(
        "name",
        "Unknown"
    )

    prompt = f"""
Analyze this news article.

SOURCE:
{source}

TITLE:
{title}

DESCRIPTION:
{description}

Return JSON with exactly this structure:

{{
    "summary": "A concise factual summary.",
    "key_points": [
        "Important point 1",
        "Important point 2",
        "Important point 3"
    ],
    "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
    ],
    "category": "technology",
    "importance": 1
}}

CATEGORY must be one of:

technology
business
world
science
politics
sports
health
entertainment
other

IMPORTANCE must be an integer from 1 to 10.
"""

    response = client.responses.create(

        model=MODEL,

        instructions=SYSTEM_PROMPT,

        input=prompt
    )

    raw_output = response.output_text.strip()

    try:

        result = json.loads(
            raw_output
        )

    except json.JSONDecodeError:

        raise ValueError(
            "OpenAI returned invalid JSON:\n"
            + raw_output
        )

    return result
from src.models import groq_client
from src.config import TEXT_MODEL


ROUTER_PROMPT = """
You are a query routing system for a Universal Multimodal RAG system.

Classify the user's question into exactly ONE category.

Categories:

TEXT
- General questions about information in documents
- Definitions
- Explanations
- Summaries
- Technical questions

TABLE
- Questions requiring numerical calculations
- Aggregations
- Sorting
- Filtering rows
- Average, sum, count, minimum, maximum
- Questions about CSV or Excel data

VISION
- Questions about images
- Charts
- Diagrams
- Visual layouts
- Objects visible in an image

AUDIO
- Questions specifically about spoken/audio content

VIDEO
- Questions requiring video content
- Video frames
- Video events
- Video speech

Return ONLY one category:

TEXT
TABLE
VISION
AUDIO
VIDEO
"""


def classify_query(query):

    response = groq_client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {
                "role": "system",
                "content": ROUTER_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0
    )

    route = response.choices[0].message.content.strip().upper()

    valid_routes = {
        "TEXT",
        "TABLE",
        "VISION",
        "AUDIO",
        "VIDEO"
    }

    if route not in valid_routes:
        route = "TEXT"

    return route
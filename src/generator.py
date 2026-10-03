from src.models import groq_client
from src.config import TEXT_MODEL


SYSTEM_PROMPT = """
You are a knowledge assistant for a multimodal RAG system.

Answer the user's question using ONLY the provided context.

Rules:

1. Do not invent information.

2. If the context does not contain the answer, say:
   "I could not find the answer in the provided documents."

3. Give a clear and concise answer.

4. When making a factual statement, include the
   supporting SOURCE_ID in this format:

   [Source 1]

5. Use only SOURCE_ID values that actually exist
   in the provided context.

6. Do not create fake source IDs.

7. At the end, provide a Sources section.
"""


def generate_answer(
    query,
    context
):

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
====================================

{context}

====================================

USER QUESTION:
{query}

ANSWER:
"""

    response = groq_client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
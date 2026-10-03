import base64
from pathlib import Path

from src.models import groq_client
from src.config import VISION_MODEL
from src.document_schema import create_document


def encode_image(file_path):

    with open(file_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


def process_image(file_path):

    file_path = Path(file_path)

    print(f"Processing image: {file_path.name}")

    # =========================
    # ENCODE IMAGE
    # =========================

    image_base64 = encode_image(file_path)

    # =========================
    # VISION MODEL
    # =========================

    response = groq_client.chat.completions.create(

        model=VISION_MODEL,

        messages=[
            {
                "role": "user",

                "content": [

                    {
                        "type": "text",

                        "text": """
Analyze this image for a multimodal RAG system.

Provide a concise but useful factual description.

If it is a chart:
- identify important values
- identify highest and lowest values
- explain the main trend

If it is a table:
- describe important rows and columns
- preserve important values

If it is a diagram:
- identify important components
- explain relationships or flow

If it is a photograph:
- describe important objects and the scene

Focus only on information useful for future question answering.
Do not add speculation.
"""
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": (
                                f"data:image/"
                                f"{file_path.suffix.replace('.', '')};"
                                f"base64,{image_base64}"
                            )
                        }
                    }
                ]
            }
        ],

        temperature=0,

        # IMPORTANT
        max_tokens=700
    )

    # =========================
    # GET DESCRIPTION
    # =========================

    description = response.choices[0].message.content

    # =========================
    # STANDARD DOCUMENT
    # =========================

    document = create_document(

        content=description,

        source=file_path.name,

        file_type="image",

        modality="vision"
    )

    print("Image processed successfully.")

    return [document]
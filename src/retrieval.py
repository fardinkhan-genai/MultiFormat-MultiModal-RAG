from langchain_chroma import Chroma

from src.models import embeddings
from src.config import (
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_COLLECTION_NAME
)


def load_vectorstore():

    print("Loading ChromaDB...")

    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    print("ChromaDB loaded successfully.")

    return vectorstore


def retrieve_documents(
    query,
    k=5
):

    vectorstore = load_vectorstore()

    print("\n====================================")
    print("RETRIEVAL")
    print("====================================")

    print(f"Query: {query}")
    print(f"Top K: {k}")

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    print(f"\nDocuments retrieved: {len(results)}")

    return results



def format_context(results):

    context_parts = []

    for index, document in enumerate(
        results,
        start=1
    ):

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        file_type = document.metadata.get(
            "file_type",
            "Unknown"
        )

        modality = document.metadata.get(
            "modality",
            "Unknown"
        )

        page = document.metadata.get(
            "page",
            "N/A"
        )

        frame = document.metadata.get(
            "frame",
            "N/A"
        )

        context_parts.append(
            f"""
SOURCE_ID: {index}

File: {source}
File Type: {file_type}
Modality: {modality}
Page: {page}
Frame: {frame}

Content:
{document.page_content}
"""
        )

    return "\n".join(context_parts)



def extract_sources(results):

    sources = []

    for index, document in enumerate(
        results,
        start=1
    ):

        source_info = {
            "source_id": index,
            "source": document.metadata.get(
                "source",
                "Unknown"
            ),
            "file_type": document.metadata.get(
                "file_type",
                "Unknown"
            ),
            "modality": document.metadata.get(
                "modality",
                "Unknown"
            ),
            "page": document.metadata.get(
                "page"
            ),
            "frame": document.metadata.get(
                "frame"
            )
        }

        sources.append(source_info)

    return sources
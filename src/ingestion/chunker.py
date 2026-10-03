from langchain_experimental.text_splitter import SemanticChunker

from src.models import embeddings


def create_semantic_chunks(documents):

    print("Starting semantic chunking...")

    splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type="percentile"
    )

    chunks = splitter.split_documents(documents)

    print(f"Original documents : {len(documents)}")
    print(f"Semantic chunks    : {len(chunks)}")

    return chunks
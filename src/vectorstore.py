from langchain_chroma import Chroma

from src.models import embeddings
from src.config import (
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_COLLECTION_NAME
)


def create_vectorstore(documents):

    print("Creating ChromaDB...")

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIRECTORY
    )

    print("ChromaDB created successfully.")

    return vectorstore
from pathlib import Path

from src.ingestion.file_router import process_file
from src.ingestion.chunker import create_semantic_chunks
from src.vectorstore import create_vectorstore


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".docx",
    ".pptx",
    ".csv",
    ".xlsx",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv"
}


def discover_files(data_directory):

    data_directory = Path(data_directory)

    files = []

    for file_path in data_directory.rglob("*"):

        if file_path.is_file():

            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:

                files.append(file_path)

    return files


def ingest_directory(data_directory):

    print("\n====================================")
    print("MULTIFORMAT INGESTION PIPELINE")
    print("====================================")

    files = discover_files(data_directory)

    print(f"\nFiles discovered: {len(files)}")

    all_documents = []

    for file_path in files:

        print(f"\nProcessing: {file_path.name}")

        documents = process_file(file_path)

        all_documents.extend(documents)

        print(
            f"Documents created: {len(documents)}"
        )

    print("\n====================================")
    print("INGESTION SUMMARY")
    print("====================================")

    print(f"Files processed     : {len(files)}")
    print(f"Documents extracted : {len(all_documents)}")

    return all_documents


def build_knowledge_base(data_directory):

    documents = ingest_directory(data_directory)

    if not documents:

        raise ValueError(
            "No supported documents found."
        )

    print("\nCreating semantic chunks...")

    chunks = create_semantic_chunks(documents)

    print(f"Total chunks: {len(chunks)}")

    print("\nCreating vector database...")

    vectorstore = create_vectorstore(chunks)

    print("\n====================================")
    print("KNOWLEDGE BASE READY")
    print("====================================")

    return vectorstore
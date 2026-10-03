from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader
)

from src.document_schema import create_document


def process_document(file_path):

    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    print(f"Processing document: {file_path.name}")

    # =========================
    # TXT
    # =========================

    if extension == ".txt":

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        documents = loader.load()


    # =========================
    # DOCX
    # =========================

    elif extension == ".docx":

        loader = Docx2txtLoader(
            str(file_path)
        )

        documents = loader.load()


    # =========================
    # PPTX
    # =========================

    elif extension == ".pptx":

        loader = UnstructuredPowerPointLoader(
            str(file_path)
        )

        documents = loader.load()


    else:

        raise ValueError(
            f"Unsupported document type: {extension}"
        )


    # =========================
    # STANDARDIZE DOCUMENTS
    # =========================

    processed_documents = []

    for document in documents:

        new_document = create_document(
            content=document.page_content,
            source=file_path.name,
            file_type=extension.replace(".", ""),
            modality="text"
        )

        processed_documents.append(new_document)


    print(
        f"Documents extracted: "
        f"{len(processed_documents)}"
    )

    return processed_documents
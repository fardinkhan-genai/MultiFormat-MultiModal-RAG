from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader

from src.document_schema import create_document


def process_pdf(file_path):
    file_path = Path(file_path)
    print(f"Processing PDF: {file_path.name}")
    loader = PyMuPDFLoader(str(file_path))
    pages = loader.load()
    documents = []

    for page in pages:
        document = create_document(
            content=page.page_content,
            source=file_path.name,
            file_type="pdf",
            modality="text",
            page=page.metadata.get("page", 0) + 1
        )

        documents.append(document)

    print(f"Pages extracted: {len(documents)}")

    return documents
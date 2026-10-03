from langchain_core.documents import Document


def create_document(
    content,
    source,
    file_type,
    modality,
    **metadata
):
    """
    Create a standardized Document for the multimodal RAG system.
    """

    document_metadata = {
        "source": source,
        "file_type": file_type,
        "modality": modality,
        **metadata
    }

    return Document(
        page_content=content,
        metadata=document_metadata
    )
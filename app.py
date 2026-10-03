import streamlit as st
from pathlib import Path
import shutil

from src.ingestion.universal_ingestion import build_knowledge_base
from src.rag import UniversalRAG


st.set_page_config(
    page_title="MultiFormat Multimodal RAG",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 MultiFormat Multimodal RAG")

st.markdown(
    """
Upload documents, images, audio, or video and ask
questions across your knowledge base.
"""
)


# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.header("Upload Files")


uploaded_files = st.sidebar.file_uploader(
    "Upload your files",
    type=[
        "pdf",
        "txt",
        "docx",
        "pptx",
        "csv",
        "xlsx",
        "jpg",
        "jpeg",
        "png",
        "webp",
        "mp3",
        "wav",
        "m4a",
        "ogg",
        "mp4",
        "avi",
        "mov",
        "mkv"
    ],
    accept_multiple_files=True
)


if uploaded_files:

    if st.sidebar.button(
        "Build Knowledge Base"
    ):

        data_directory = Path("data/uploads")

        data_directory.mkdir(
            parents=True,
            exist_ok=True
        )


        # Save uploaded files

        for uploaded_file in uploaded_files:

            file_path = (
                data_directory
                / uploaded_file.name
            )

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )


        with st.spinner(
            "Processing files and building knowledge base..."
        ):

            build_knowledge_base(
                data_directory
            )


        st.sidebar.success(
            "Knowledge base created!"
        )


# ------------------------------------------------
# QUESTION
# ------------------------------------------------

st.header("Ask Your Knowledge Base")


query = st.text_input(
    "Enter your question",
    placeholder="What is Machine Learning?"
)


if st.button("Ask Question"):

    if not query:

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching knowledge base..."
        ):

            rag = UniversalRAG()

            result = rag.ask(
                query
            )


        # ----------------------------------------
        # ANSWER
        # ----------------------------------------

        st.subheader("Answer")

        st.write(
            result["answer"]
        )


        # ----------------------------------------
        # SOURCES
        # ----------------------------------------

        st.subheader("Sources")


        for source in result["sources"]:

            source_text = (
                f"**{source['source_id']}. "
                f"{source['source']}**"
            )

            st.markdown(
                source_text
            )


            details = []

            if source.get("file_type"):

                details.append(
                    f"Type: {source['file_type']}"
                )

            if source.get("modality"):

                details.append(
                    f"Modality: {source['modality']}"
                )

            if source.get("page"):

                details.append(
                    f"Page: {source['page']}"
                )

            if source.get("frame"):

                details.append(
                    f"Frame: {source['frame']}"
                )


            if details:

                st.caption(
                    " | ".join(details)
                )
from groq import Groq
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import (
    GROQ_API_KEY,
    EMBEDDING_MODEL
)


# =========================
# GROQ CLIENT
# =========================

groq_client = Groq(
    api_key=GROQ_API_KEY
)


# =========================
# EMBEDDING MODEL
# =========================

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)
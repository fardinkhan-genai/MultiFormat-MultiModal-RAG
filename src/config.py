import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# API CONFIGURATION
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# =========================
# MODEL CONFIGURATION
# =========================

TEXT_MODEL = "openai/gpt-oss-20b"
VISION_MODEL = "qwen/qwen3.8-27b"
STT_MODEL = "whisper-large-v3-turbo"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# =========================
# CHROMA CONFIGURATION
# =========================

CHROMA_PERSIST_DIRECTORY = "./chroma_db"
CHROMA_COLLECTION_NAME = "multiformat_multimodal_rag"
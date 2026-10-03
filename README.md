# MultiFormat MultiModal RAG

An end-to-end **Multi-Format Multimodal Retrieval-Augmented Generation
(RAG)** system for uploading documents, images, audio, and video,
building a unified knowledge base, and asking natural-language questions
with source-aware answers.

## 🚀 Overview

This project extends traditional RAG beyond PDF/text-only workflows.

### Supported formats

-   PDF
-   TXT
-   DOCX
-   PPTX
-   CSV
-   XLSX
-   JPG / JPEG / PNG / WEBP
-   MP3 / WAV / M4A / OGG
-   MP4 / AVI / MOV / MKV

The system routes each file to a modality-specific processor, converts
the extracted information into a common LangChain `Document`, performs
semantic chunking, generates embeddings, stores them in ChromaDB,
retrieves relevant information using hybrid search, reranks the
candidates, and generates a grounded answer using an LLM.

------------------------------------------------------------------------

## 🏗️ Architecture

``` text
                         USER FILES
                             │
                             ▼
                    ┌─────────────────┐
                    │   FILE ROUTER   │
                    └────────┬────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │          │          │          │           │
       ▼          ▼          ▼          ▼           ▼
      PDF      DOCX/PPTX    CSV/XLSX   IMAGE      AUDIO/VIDEO
       │          │          │          │           │
       │          │          │        Qwen        Whisper
       │          │          │        Vision         │
       │          │          │          │            │
       └──────────┴──────────┴──────────┴────────────┘
                             │
                             ▼
                   LANGCHAIN DOCUMENTS
                             │
                             ▼
                   SEMANTIC CHUNKING
                             │
                             ▼
                  MINILM EMBEDDINGS
                             │
                             ▼
                       CHROMADB
                             │
                       USER QUERY
                             │
                             ▼
                ┌──────────────────────┐
                │   HYBRID RETRIEVAL   │
                │   Chroma + BM25      │
                └──────────┬───────────┘
                           │
                           ▼
                    CROSS-ENCODER
                      RERANKER
                           │
                           ▼
                    RELEVANT CONTEXT
                           │
                           ▼
                    GROQ GPT-OSS-20B
                           │
                           ▼
                  ANSWER + SOURCES
                           │
                           ▼
                     STREAMLIT UI
```

------------------------------------------------------------------------

## ✨ Key Features

### Multi-Format Ingestion

  Format   Processing
  -------- ----------------------------
  PDF      PyMuPDF
  TXT      LangChain TextLoader
  DOCX     Docx2txtLoader
  PPTX     PowerPoint document loader
  CSV      Pandas
  XLSX     Pandas
  Images   Qwen Vision
  Audio    Whisper
  Video    Whisper + Qwen Vision

### Multimodal Processing

-   **Qwen Vision** analyzes images and extracted video frames.
-   **Whisper** converts audio and video speech into text.
-   Transcripts and visual descriptions become searchable RAG content.

### Semantic Chunking

Uses LangChain `SemanticChunker` to split documents according to
semantic boundaries.

### Vector Search

Uses:

``` text
sentence-transformers/all-MiniLM-L6-v2
```

for embeddings and **ChromaDB** for persistent vector storage.

### Hybrid Retrieval

Combines:

-   Vector similarity search
-   BM25 keyword search

This supports both semantic questions and exact terminology, names,
values, and technical terms.

### Reranking

Retrieved candidates are reranked using:

``` text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

### Grounded Generation

The final answer is generated using:

``` text
openai/gpt-oss-20b
```

through Groq.

The generation pipeline uses retrieved context and instructs the model
not to invent information outside the provided context.

### Source-Aware Answers

Retrieved documents preserve metadata such as:

-   Source filename
-   File type
-   Modality
-   Page number
-   Video frame information where available

### Streamlit Interface

The application provides:

1.  File upload
2.  Knowledge-base creation
3.  Natural-language question answering
4.  Source display

------------------------------------------------------------------------

## 🧰 Technology Stack

### GenAI / LLM

-   Groq
-   GPT-OSS-20B
-   Qwen Vision
-   Whisper

### RAG

-   LangChain
-   Semantic Chunking
-   Hybrid Retrieval
-   BM25
-   Cross-Encoder Reranking

### Embeddings

``` text
sentence-transformers/all-MiniLM-L6-v2
```

### Vector Database

-   ChromaDB

### Document Processing

-   PyMuPDF
-   Docx2txt
-   PowerPoint loaders
-   Pandas
-   OpenPyXL

### Multimedia

-   Pillow
-   OpenCV
-   FFmpeg

### UI

-   Streamlit

------------------------------------------------------------------------

## 📁 Project Structure

``` text
Universal_Multimodal_RAG/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
│
├── data/
│   ├── pdf/
│   ├── documents/
│   ├── tabular/
│   ├── images/
│   ├── audio/
│   ├── video/
│   └── uploads/
│
├── chroma_db/
│
└── src/
    ├── config.py
    ├── models.py
    ├── document_schema.py
    ├── vectorstore.py
    ├── retrieval.py
    ├── hybrid_retrieval.py
    ├── reranker.py
    ├── generator.py
    ├── rag.py
    │
    └── ingestion/
        ├── pdf_processor.py
        ├── document_processor.py
        ├── tabular_processor.py
        ├── image_processor.py
        ├── audio_processor.py
        ├── video_processor.py
        ├── file_router.py
        ├── chunker.py
        └── universal_ingestion.py
```

------------------------------------------------------------------------

## ⚙️ Setup

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Multiformat_Multimodal_RAG
```

### 2. Create a virtual environment

Windows:

``` bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

``` bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create `.env`:

``` env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env` to GitHub.

### 5. Install FFmpeg

Video processing requires FFmpeg.

Verify:

``` bash
ffmpeg -version
```

------------------------------------------------------------------------

## ▶️ Run the Application

Start Streamlit:

``` bash
streamlit run app.py
```

Then open the local URL displayed in the terminal.

------------------------------------------------------------------------

## 🔄 Workflow

``` text
Upload Files
     ↓
File Router
     ↓
Format-Specific Processing
     ↓
Common LangChain Documents
     ↓
Semantic Chunking
     ↓
MiniLM Embeddings
     ↓
ChromaDB
     ↓
User Question
     ↓
Vector Search + BM25
     ↓
Cross-Encoder Reranking
     ↓
Relevant Context
     ↓
GPT-OSS-20B
     ↓
Answer + Sources
```

------------------------------------------------------------------------

## 🔐 Environment Variables

  Variable         Description
  ---------------- -------------------------
  `GROQ_API_KEY`   API key for Groq models

Example:

``` env
GROQ_API_KEY=your_groq_api_key_here
```

For GitHub, provide a `.env.example` instead:

``` env
GROQ_API_KEY=your_groq_api_key_here
```

------------------------------------------------------------------------

## 📌 Recommended `.gitignore`

``` gitignore
.venv/
.env
__pycache__/
*.pyc

chroma_db/
data/
.ipynb_checkpoints/
```

------------------------------------------------------------------------

## 🎯 Project Objectives

This project demonstrates an end-to-end implementation of:

-   Multimodal data ingestion
-   RAG architecture
-   Semantic chunking
-   Vector embeddings
-   Vector databases
-   Hybrid retrieval
-   BM25 keyword search
-   Cross-encoder reranking
-   LLM-based answer generation
-   Vision-language processing
-   Speech-to-text processing
-   Source-aware responses
-   Streamlit application development

------------------------------------------------------------------------

## 💡 Example Questions

Depending on the uploaded knowledge base:

``` text
What is Machine Learning?

Summarize the main points in this document.

What does this architecture diagram show?

What did the speaker discuss about transformers?

What are the important findings in the report?

Which source contains information about this topic?
```

------------------------------------------------------------------------

## 🚧 Current Limitations

-   Large datasets may require more optimized ingestion.
-   Video frame sampling is currently interval-based.
-   Audio/video timestamp handling can be further refined.
-   Tabular data currently participates in the searchable RAG pipeline
    rather than a dedicated SQL/Pandas reasoning agent.
-   Authentication and multi-user deployment are outside the current
    scope.
-   The project is primarily designed as a local/portfolio application.

------------------------------------------------------------------------

## 🔮 Future Improvements

Possible future extensions:

-   Timestamp-aware video retrieval
-   Dedicated table analytics
-   Advanced multimodal retrieval
-   RAG evaluation
-   Response streaming
-   Cloud deployment
-   Authentication
-   Production monitoring and tracing

------------------------------------------------------------------------

## 👨‍💻 Author

**Fardin Khan**

Data Science & AI Engineer Developer

Focus areas:

-   Generative AI
-   RAG
-   Multimodal RAG
-   Agentic AI
-   Machine Learning
-   Deep Learning
-   Python

------------------------------------------------------------------------

## ⭐ Project Status

``` text
Multi-format ingestion     ✅
Multimodal processing      ✅
Semantic chunking          ✅
ChromaDB                   ✅
Hybrid retrieval           ✅
Reranking                  ✅
Source-aware generation    ✅
Streamlit UI               ✅

PROJECT COMPLETE
```

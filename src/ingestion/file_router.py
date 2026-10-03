from pathlib import Path

from src.ingestion.pdf_processor import process_pdf
from src.ingestion.document_processor import process_document
from src.ingestion.tabular_processor import process_tabular
from src.ingestion.image_processor import process_image
from src.ingestion.audio_processor import process_audio
from src.ingestion.video_processor import process_video


def process_file(file_path):

    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    print("\n====================================")
    print(f"File: {file_path.name}")
    print(f"Type: {extension}")
    print("====================================")

    if extension == ".pdf":

        return process_pdf(file_path)

    elif extension in [".txt", ".docx", ".pptx"]:

        return process_document(file_path)

    elif extension in [".csv", ".xlsx"]:

        return process_tabular(file_path)

    elif extension in [".jpg", ".jpeg", ".png", ".webp"]:

        return process_image(file_path)

    elif extension in [".mp3", ".wav", ".m4a", ".ogg"]:

        return process_audio(file_path)

    elif extension in [".mp4", ".avi", ".mov", ".mkv"]:

        return process_video(file_path)

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )
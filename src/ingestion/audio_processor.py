from pathlib import Path

from src.models import groq_client
from src.config import STT_MODEL
from src.document_schema import create_document


def process_audio(file_path):

    file_path = Path(file_path)

    print(f"Processing audio: {file_path.name}")


    # =========================
    # SPEECH TO TEXT
    # =========================

    with open(file_path, "rb") as audio_file:

        transcription = groq_client.audio.transcriptions.create(
            file=audio_file,
            model=STT_MODEL,
            response_format="verbose_json"
        )


    transcript = transcription.text


    # =========================
    # STANDARD DOCUMENT
    # =========================

    document = create_document(

        content=transcript,

        source=file_path.name,

        file_type="audio",

        modality="audio"
    )


    print("Audio transcription completed.")

    return [document]
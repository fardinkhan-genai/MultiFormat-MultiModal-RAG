from pathlib import Path
import subprocess
import tempfile

from src.ingestion.audio_processor import process_audio
from src.ingestion.image_processor import process_image


def extract_audio(video_path, audio_path):

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "mp3",
        str(audio_path)
    ]

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def extract_frames(video_path, output_directory, interval=30):

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_pattern = output_directory / "frame_%05d.jpg"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vf",
        f"fps=1/{interval}",
        str(output_pattern)
    ]

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def process_video(file_path):

    file_path = Path(file_path)

    print(f"Processing video: {file_path.name}")

    documents = []

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_dir = Path(temp_dir)

        # =========================
        # AUDIO EXTRACTION
        # =========================

        audio_path = temp_dir / "audio.mp3"

        extract_audio(
            file_path,
            audio_path
        )

        audio_documents = process_audio(
            audio_path
        )

        for document in audio_documents:

            document.metadata.update({
                "source": file_path.name,
                "file_type": "video",
                "modality": "video_audio"
            })

        documents.extend(audio_documents)


        # =========================
        # FRAME EXTRACTION
        # =========================

        frames_directory = temp_dir / "frames"

        extract_frames(
            file_path,
            frames_directory,
            interval=30
        )


        # =========================
        # PROCESS FRAMES
        # =========================

        frame_files = sorted(
            frames_directory.glob("*.jpg")
        )

        for frame_file in frame_files:

            frame_documents = process_image(
                frame_file
            )

            for document in frame_documents:

                document.metadata.update({
                    "source": file_path.name,
                    "file_type": "video",
                    "modality": "video_frame",
                    "frame": frame_file.name
                })

            documents.extend(frame_documents)


    print(
        f"Video documents created: {len(documents)}"
    )

    return documents
from pathlib import Path

import pandas as pd

from src.document_schema import create_document


def process_tabular(file_path):

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    print(f"Processing tabular file: {file_path.name}")


    # =========================
    # CSV
    # =========================

    if extension == ".csv":

        df = pd.read_csv(file_path)


    # =========================
    # EXCEL
    # =========================

    elif extension == ".xlsx":

        df = pd.read_excel(file_path)


    else:

        raise ValueError(
            f"Unsupported tabular file type: {extension}"
        )


    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    print("\nColumns:")
    print(list(df.columns))


    # =========================
    # DATAFRAME → TEXT
    # =========================

    content = df.to_markdown(
        index=False
    )


    # =========================
    # STANDARD DOCUMENT
    # =========================

    document = create_document(
        content=content,
        source=file_path.name,
        file_type=extension.replace(".", ""),
        modality="table",
        rows=len(df),
        columns=len(df.columns)
    )


    return [document]
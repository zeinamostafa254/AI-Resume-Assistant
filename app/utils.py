import shutil
from pathlib import Path
from fastapi import UploadFile


UPLOAD_DIR = Path(
    "data/uploaded_files"
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}


def validate_file_type(
    filename,
):

    extension = Path(
        filename
    ).suffix.lower()

    return (
        extension
        in ALLOWED_EXTENSIONS
    )


def save_uploaded_file(
    file: UploadFile,
):

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not validate_file_type(
        file.filename
    ):

        raise ValueError(
            "Only PDF and DOCX files are allowed."
        )

    file_path = (
        UPLOAD_DIR
        / file.filename
    )

    with open(
        file_path,
        "wb",
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return file_path


def clear_uploaded_files():

    if not UPLOAD_DIR.exists():

        return

    for file in (
        UPLOAD_DIR.iterdir()
    ):

        file.unlink()
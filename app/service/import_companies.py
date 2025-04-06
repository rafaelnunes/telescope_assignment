from typing import BinaryIO

from core.exceptions import TelescopeValidationException
from fastapi import UploadFile


def import_company(file: UploadFile) -> int:
    if file.content_type == "text/csv":
        return import_csv(file.file)
    elif file.content_type == "application/json":
        return import_json(file.file)
    else:
        raise TelescopeValidationException(f"Unsupported file type: {file.content_type}")


def import_csv(file: BinaryIO):
    processed = [1, 1]
    return len(processed)


def import_json(file: BinaryIO):
    processed = [1]

    return len(processed)

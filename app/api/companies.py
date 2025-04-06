"""Companies API"""

from typing import List

from core.exceptions import TelescopeValidationException
from fastapi import APIRouter, UploadFile
from service.import_companies import import_company


router = APIRouter(tags=["companies"])


@router.post("/import_company_data")
async def import_company_data(
    file: UploadFile,
):
    """Import company data from a file.

    Args:
        file: The file to import.
    """
    SUPPORTED_FILE_TYPES = ["text/csv", "application/json"]
    assert file.content_type in SUPPORTED_FILE_TYPES, f"Unsupported file type: {file.content_type}"
    if file.content_type not in SUPPORTED_FILE_TYPES:
        raise TelescopeValidationException(msg="Unsupported file type")

    imported_count = import_company(file)
    return {"imported_records": imported_count}


@router.post("/process_company")
async def process_company(urls: List[str]):
    pass


@router.get("/get_companies")
async def get_companies():
    return {"message": "Companies fetched successfully"}

"""Companies API"""

from api.deps import DBSession
from api.schema import ProcessCompanyRequest
from core.exceptions import TelescopeValidationException
from fastapi import APIRouter, UploadFile
from service.companies import get_processed_companies, import_company, process_companies


router = APIRouter(tags=["companies"])


@router.post("/import_company_data")
async def import_company_data(
    file: UploadFile,
    db_session: DBSession,
):
    """Import company data from a file.

    Args:
        file: The file to import.
        db_session: Database session.
    """
    SUPPORTED_FILE_TYPES = ["text/csv", "application/json"]
    assert file.content_type in SUPPORTED_FILE_TYPES, f"Unsupported file type: {file.content_type}"
    if file.content_type not in SUPPORTED_FILE_TYPES:
        raise TelescopeValidationException(msg="Unsupported file type")

    imported_count = await import_company(file, db_session)
    return {"imported_records": imported_count}


@router.post("/process_company")
async def process_company(process_request: ProcessCompanyRequest, db_session: DBSession):
    """Process the company for a given rule.

    Args:
        request: The request to process the company.
    """
    processed_data = await process_companies(
        process_request.urls, process_request.rules, db_session
    )
    return processed_data


@router.get("/get_companies")
async def get_companies(db_session: DBSession):
    """Get all companies.

    Args:
        db_session: Database session.
    """
    companies = await get_processed_companies(db_session)
    return companies

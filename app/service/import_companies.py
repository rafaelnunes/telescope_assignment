"""Import companies from a file."""

import csv
import datetime
import io
import json
from typing import Any, Dict, List

from core.exceptions import TelescopeValidationException
from core.logging import get_logger
from fastapi import UploadFile
from models.companies import CompanyData
from sqlalchemy.orm import Session


logger = get_logger(__name__)


async def import_company(file: UploadFile, db_session: Session) -> int:
    """Import companies from a file."""
    if file.content_type == "text/csv":
        company_data = await _parse_csv(file)
    elif file.content_type == "application/json":
        company_data = await _parse_json(file)
    else:
        raise TelescopeValidationException(f"Unsupported file type: {file.content_type}")

    processed_data = 0
    for company in company_data:
        try:
            import_company_data(company, db_session)
            processed_data += 1
        except Exception as e:
            logger.error(f"Error importing company: {e}")

    return processed_data


def import_company_data(company_data: dict, db_session: Session) -> dict:
    """Import company data."""
    growth = {
        "2Y": company_data.get("employee_growth_2Y", ""),
        "1Y": company_data.get("employee_growth_1Y", ""),
        "6M": company_data.get("employee_growth_6M", ""),
    }
    company = CompanyData(
        name=company_data["company_name"],
        url=company_data["url"],
        description=company_data["description"],
        industry=company_data["industry"],
        founded_year=company_data["founded_year"],
        total_employees=company_data["total_employees"],
        headquarters_city=company_data["headquarters_city"],
        employee_locations=company_data["employee_locations"],
        employee_growth=growth,
        imported_at=datetime.datetime.now(),
    )
    db_session.add(company)
    db_session.commit()
    return company


async def _parse_csv(file: UploadFile) -> List[Dict[str, Any]]:
    """Import companies from a CSV file asynchronously."""
    # Read the file content
    content = await file.read()
    # Decode the content
    text_content = content.decode("utf-8")
    # Create a StringIO object to use with csv.DictReader
    csv_file = io.StringIO(text_content)
    # Parse the CSV
    reader = csv.DictReader(csv_file)
    # Convert to list
    return list(reader)


async def _parse_json(file: UploadFile) -> List[Dict[str, Any]]:
    """Import companies from a JSON file asynchronously."""
    # Read the file content
    content = await file.read()
    # Parse the JSON
    return json.loads(content)

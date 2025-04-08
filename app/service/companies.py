"""Import companies from a file."""

import csv
import datetime
import io
import json
from typing import Any, Dict, List

from api.schema import ProcessedCompaniesOutput, Rule
from core.exceptions import TelescopeValidationException
from core.logging import get_logger
from fastapi import UploadFile
from models.companies import CompanyData, ProcessedCompany
from service.rules import get_feature_value
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


logger = get_logger(__name__)

# Common SaaS keywords in descriptions - simplified to match more variations
SAAS_KEYWORDS = {
    "subscription",
    "monthly",
    "annual",
    "per-user",
    "per user",
    "per-seat",
    "per seat",
    "usage based",
    "usage-based",
    "tier",
    "tiered",
    "cloud",
    "cloud-based",
    "cloud platform",
    "saas",
    "software as a service",
    "license",
    "licensing",
    "recurring",
}


def is_saas_company(industry: str, description: str) -> bool:
    """Determine if a company is a SaaS company based on description keywords.

    Args:
        industry: The company's industry (not used in this implementation)
        description: The company's description

    Returns:
        bool: True if the company appears to be a SaaS company based on keywords
    """
    if not description:
        return False

    # Convert to lowercase for case-insensitive matching
    description_lower = description.lower()

    # Count how many SaaS keywords appear in the description
    keyword_matches = sum(1 for keyword in SAAS_KEYWORDS if keyword in description_lower)

    # Consider it a SaaS company if it has 2 or more SaaS keywords
    return keyword_matches >= 1


async def import_company(file: UploadFile, db_session: AsyncSession) -> int:
    """Import companies from a file.

    Args:
        file: The file to import.
        db_session: The database session.

    Returns:
        The imported company data.
    """
    if file.content_type == "text/csv":
        company_data = await _parse_csv(file)
    elif file.content_type == "application/json":
        company_data = await _parse_json(file)
    else:
        raise TelescopeValidationException(f"Unsupported file type: {file.content_type}")

    processed_data = 0
    for company in company_data:
        try:
            await import_company_data(company, db_session)
            processed_data += 1
        except Exception as e:
            logger.error(f"Error importing company: {e}")

    return processed_data


async def import_company_data(
    company_data: Dict[str, Any], db_session: AsyncSession
) -> CompanyData:
    """Import company data.

    Args:
        company_data: The company data to import.
        db_session: The database session.

    Returns:
        The imported company data.
    """
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
        founded_year=int(company_data["founded_year"]),
        total_employees=int(company_data["total_employees"]),
        headquarters_city=company_data["headquarters_city"],
        employee_locations=company_data["employee_locations"],
        employee_growth=growth,
        imported_at=datetime.datetime.now(),
        extras={},
    )

    extras = {
        "company_age": datetime.datetime.now().year - company.founded_year,
        "is_usa_based": "(USA)" in company.headquarters_city,
        "is_saas": is_saas_company(company.industry, company.description),
    }
    company.extras = extras
    db_session.add(company)
    await db_session.commit()
    return company


async def _parse_csv(file: UploadFile) -> List[Dict[str, Any]]:
    """Import companies from a CSV file asynchronously.

    Args:
        file: The file to import.

    Returns:
        A list of dictionaries containing the company data.
    """
    content = await file.read()
    csv_file = io.StringIO(content.decode("utf-8"))
    return list(csv.DictReader(csv_file))


async def _parse_json(file: UploadFile) -> List[Dict[str, Any]]:
    """Import companies from a JSON file asynchronously.

    Args:
        file: The file to import.

    Returns:
        A list of dictionaries containing the company data.
    """
    content = await file.read()

    return json.loads(content)


async def process_companies(
    urls: list[str], rules: list[Rule], db_session: AsyncSession
) -> ProcessedCompaniesOutput:
    """Process the companies for a given rule.

    Args:
        urls: The URLs to process.
        rules: The rules to process.
        db_session: The database session.
    Returns:
        A list of dictionaries containing the processed company data.
    """
    processed_data = []
    for url in urls:
        company = await get_company_by_url(url, db_session)
        if company is None:
            raise TelescopeValidationException(f"Company not found: {url}")

        processed_company = await process_company(company, rules, db_session)
        processed_data.append(
            {
                **processed_company.data,
            }
        )
    await db_session.commit()

    return ProcessedCompaniesOutput(root=processed_data)


async def get_company_by_url(url: str, db_session: AsyncSession) -> CompanyData:
    """Get the company by URL.

    Args:
        url: The URL to get the company by.

    Returns:
        The company data.
    """
    company = await db_session.exec(select(CompanyData).where(CompanyData.url == url))
    return company.first()


async def process_company(
    company: CompanyData, rules: list[Rule], db_session: AsyncSession
) -> ProcessedCompany:
    """Process the company for a given rule.

    Args:
        company: The company to process.
        rules: The rules to process.
        db_session: The database session.

    Returns:
        A dictionary containing the processed company data.
    """
    company_processed_data = {
        "company_name": company.name,
    }
    for rule in rules:
        feature_value = get_feature_value(company, rule)
        company_processed_data.update(feature_value)

    existing_processed = await db_session.exec(
        select(ProcessedCompany).where(ProcessedCompany.company_id == company.id)
    )
    existing = existing_processed.first()

    if existing:
        existing.data = company_processed_data
        existing.processed_at = datetime.datetime.now()
        processed_company = existing
    else:
        processed_company = ProcessedCompany(
            company_id=company.id, data=company_processed_data, processed_at=datetime.datetime.now()
        )
        db_session.add(processed_company)

    return processed_company


async def get_processed_companies(db_session: AsyncSession) -> ProcessedCompaniesOutput:
    """Get the processed companies.

    Args:
        db_session: The database session.

    Returns:
        A list of processed companies.
    """
    processed_companies = await db_session.exec(select(ProcessedCompany))
    processed_data = [
        {
            **pd.data,
        }
        for pd in processed_companies.all()
    ]

    return ProcessedCompaniesOutput(root=processed_data)

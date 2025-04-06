import datetime
import uuid

from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class UUIDModel(SQLModel):
    """Base class with integer primary key and uuid field"""

    id: int = Field(default=None, primary_key=True)
    ref_id: uuid.UUID = Field(default_factory=uuid.uuid4)


class CompanyData(UUIDModel, table=True):
    __tablename__ = "companies"

    name: str = Field(nullable=False)
    url: str = Field(nullable=False)
    description: str = Field(nullable=True)
    industry: str = Field(nullable=True)
    founded_year: int = Field(nullable=False)
    total_employees: int = Field(nullable=False)
    headquarters_city: str = Field(nullable=False)
    employee_locations: dict = Field(sa_column=Column(JSON))
    employee_growth: dict = Field(sa_column=Column(JSON))
    imported_at: datetime.datetime = Field(nullable=False)

    processed_data: list["ProcessedCompany"] = Relationship(back_populates="company")


class ProcessedCompany(UUIDModel, table=True):
    __tablename__ = "processed_companies"

    company_id: int = Field(foreign_key="companies.id")
    company: CompanyData = Relationship(back_populates="processed_data")
    data: dict = Field(sa_column=Column(JSON))
    processed_at: datetime.datetime = Field(nullable=False)

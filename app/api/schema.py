"""API Pydantic schemas"""

from typing import Any, Dict, List

import pydantic


class RuleOperation(pydantic.BaseModel):
    """Schema for rule operation"""

    greater_than: float | None = None
    less_than: float | None = None
    equal: Any | None = None


class Rule(pydantic.BaseModel):
    """Schema for individual rule"""

    input: str
    feature_name: str
    operation: RuleOperation
    match: int
    default: int


class ProcessCompanyRequest(pydantic.BaseModel):
    """Request schema for processing companies"""

    urls: List[str]
    rules: List[Rule]


class ProcessedCompaniesOutput(pydantic.RootModel):
    """Output schema for processed companies"""

    root: List[Dict[str, Any]]

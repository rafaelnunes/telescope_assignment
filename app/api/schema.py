"""API Pydantic schemas"""

import pydantic


class ProcessCompanyRequest(pydantic.BaseModel):
    """Request schema for processing companies"""

    urls: list[str]
    rules: str = pydantic.Field(
        description="JSON string containing processing rules",
        json_schema_extra={"example": '{"key": "value"}'},
    )

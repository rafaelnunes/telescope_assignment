"""Rules processing service"""

from typing import Any

from api.schema import Rule
from models.companies import CompanyData


_operations = {
    "greater_than": lambda actual, value, match, default: match if actual > value else default,
    "less_than": lambda actual, value, match, default: match if actual < value else default,
    "equal": lambda actual, value, match, default: match if actual == value else default,
}


def get_feature_value(company: CompanyData, rule: Rule) -> dict[str, Any]:
    """Get the feature value for a given operation.

    Args:
        company: The company to get the feature value for.
        rule: The rule to get the feature value for.

    Returns:
        The feature value.
    """
    # Get the operation type (first non-None value)
    operation_name = next(
        (name for name, value in rule.operation.model_dump().items() if value is not None), None
    )

    if operation_name is None:
        raise ValueError("No operation specified in rule")

    # Get the actual value from company or extras
    actual = None
    if hasattr(company, rule.input):
        actual = getattr(company, rule.input)
    elif rule.input in company.extras:
        actual = company.extras[rule.input]
    else:
        raise ValueError(f"Input {rule.input} not found in company or extras")

    # Get the operation value
    operation_value = getattr(rule.operation, operation_name)

    # Apply the operation
    operation = _operations[operation_name](actual, operation_value, rule.match, rule.default)

    return {rule.feature_name: operation}

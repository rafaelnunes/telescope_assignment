#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, Optional

import requests


def get_companies(filters: Optional[Dict[str, Any]] = None) -> None:
    """
    Get companies from the /get_companies endpoint with optional filters.

    Args:
        filters: Optional dictionary of filters to apply to the query
    """
    # API endpoint
    url = "http://localhost:8000/get_companies"

    try:
        # Make the GET request
        response = requests.get(url, params=filters)

        # Check if the request was successful
        response.raise_for_status()

        # Print the response
        result = response.json()

        # Pretty print the JSON response
        print(json.dumps(result, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response text: {e.response.text}")
        sys.exit(1)


if __name__ == "__main__":
    # Example filters - can be modified or passed as command line arguments
    filters = None

    # If command line arguments are provided, use them as filters
    if len(sys.argv) > 1:
        try:
            # Expect JSON string as argument
            filters = json.loads(sys.argv[1])
            print(f"Using filters: {filters}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for filters")
            print('Usage: ./get_companies.py \'{"key": "value"}\'')
            sys.exit(1)

    get_companies(filters)

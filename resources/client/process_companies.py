#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import requests


def process_companies(rules_path: str) -> None:
    """
    Process companies using rules from a JSON file via the /process_company endpoint.

    Args:
        rules_path: Path to the JSON file containing processing rules
    """
    # Get the absolute path of the rules file
    rules_file = Path(rules_path).resolve()
    if not rules_file.exists():
        print(f"Error: File {rules_file} not found")
        sys.exit(1)

    # Read the rules file
    try:
        with open(rules_file, "r") as f:
            rules = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing rules file: {e}")
        sys.exit(1)

    # API endpoint
    url = "http://localhost:8000/process_company"

    try:
        # Make the POST request
        response = requests.post(url, json=rules)

        # Check if the request was successful
        response.raise_for_status()

        # Print the response
        result = response.json()
        print("Successfully processed companies")
        print(f"Response: {result}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response text: {e.response.text}")
        sys.exit(1)


if __name__ == "__main__":
    # Get the path to the rules file
    if len(sys.argv) > 1:
        rules_path = sys.argv[1]
    else:
        # Default to the rules.json in the resources directory
        rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rules.json")

    process_companies(rules_path)

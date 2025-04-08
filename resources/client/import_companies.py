#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import requests


def import_companies(csv_path: str) -> None:
    """
    Import companies from CSV file using the /import_company_data endpoint.

    Args:
        csv_path: Path to the CSV file containing company data
    """
    # Get the absolute path of the CSV file
    csv_file = Path(csv_path).resolve()
    if not csv_file.exists():
        print(f"Error: File {csv_file} not found")
        sys.exit(1)

    # API endpoint
    url = "http://localhost:8000/import_company_data"

    # Prepare the file for upload
    files = {"file": ("company-dataset.csv", open(csv_file, "rb"), "text/csv")}

    try:
        # Make the POST request
        response = requests.post(url, files=files)

        # Check if the request was successful
        response.raise_for_status()

        # Print the response
        result = response.json()
        print(f"Successfully imported {result.get('imported_records', 0)} records")
        print(f"Response: {result}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response text: {e.response.text}")
        sys.exit(1)
    finally:
        # Close the file
        files["file"][1].close()


if __name__ == "__main__":
    # Get the path to the CSV file
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        # Default to the company-dataset.csv in the resources directory
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "company-dataset.csv")

    import_companies(csv_path)

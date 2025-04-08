import json

from fastapi.testclient import TestClient


def test_import_company_csv(client: TestClient):
    """Test importing company from CSV."""
    # Create file data
    with open("app/tests/csv-dataset.csv", "rb") as f:
        files = {"file": ("test.csv", f.read(), "text/csv")}

    # Send request
    response = client.post(
        "/companies/import_company_data", files=files, headers={"accept": "application/json"}
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["imported_records"] == 10


def test_import_company_json(client: TestClient):
    """Test importing company from JSON."""
    # Create file data
    with open("app/tests/json-dataset.json", "rb") as f:
        files = {"file": ("test.json", f.read(), "application/json")}
    response = client.post(
        "/companies/import_company_data", files=files, headers={"accept": "application/json"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["imported_records"] == 10


def test_process_company(client: TestClient):
    """Test processing company."""
    with open("app/tests/rules.json", "r") as f:
        json_rules = f.read()
    json_rules = json.loads(json_rules)
    response = client.post(
        "/companies/process_company", json=json_rules, headers={"accept": "application/json"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10

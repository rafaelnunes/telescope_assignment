import pytest
from api.companies import router as companies_router
from api.health import router as health_router
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    # Include routers
    app.include_router(companies_router, prefix="/companies")
    app.include_router(health_router)

    return TestClient(app)

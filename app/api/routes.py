from api import companies, health
from fastapi import FastAPI


def register_routes(app: FastAPI) -> None:
    app.include_router(companies.router)
    app.include_router(health.router)

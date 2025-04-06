from api import companies
from fastapi import FastAPI


def register_routes(app: FastAPI) -> None:
    app.include_router(companies.router)

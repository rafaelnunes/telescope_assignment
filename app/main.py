import logging
from contextlib import asynccontextmanager

from api import routes
from core.config import settings
from core.exceptions import (
    ObjectNotFound,
    TelescopeException,
    TelescopeValidationException,
)
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


# Configure logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events for the FastAPI application."""
    # Startup
    logger.info("Starting up...")
    yield


def create_service() -> FastAPI:
    tags_metadata = [
        {
            "name": "health",
            "description": "Health check for api",
        },
        {
            "name": "companies",
            "description": "Companies API",
        },
    ]

    app = FastAPI(
        title="telescope-assignment",
        description="Telescope Assignment",
        version="1.0.0",
        openapi_url="/openapi.json",
        openapi_tags=tags_metadata,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routes.register_routes(app)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.errors()}
        )

    @app.exception_handler(TelescopeValidationException)
    async def telescope_validation_exception_handler(
        request: Request, exc: TelescopeValidationException
    ):
        logger.error(f"Validation error: {exc.msg}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.msg})

    @app.exception_handler(ObjectNotFound)
    async def object_not_found_exception_handler(request: Request, exc: ObjectNotFound):
        error_msg = str(exc)
        logger.error(f"Object not found: {error_msg}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": error_msg})

    @app.exception_handler(TelescopeException)
    async def telescope_exception_handler(request: Request, exc: TelescopeException):
        error_msg = str(exc)
        logger.error(f"Telescope error: {error_msg}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": error_msg}
        )

    return app


app = create_service()

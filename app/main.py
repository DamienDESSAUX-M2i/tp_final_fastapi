from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.core.database import Base, get_engine
from app.core.settings import get_settings
from app.routers import (
    auth,
    private_match,
    private_players,
    private_team,
    private_user,
    public,
)
from app.utils.set_up_log import get_logger, set_up_logging


def create_app() -> FastAPI:
    """Application factory."""

    settings = get_settings()

    log_config_path = Path(settings.log_config_path).resolve()
    set_up_logging(log_config_path)
    logger = get_logger(__name__)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifecycle manager."""

        logger.info("Application startup")

        logger.info("Database initialization")
        engine = get_engine()
        Base.metadata.create_all(bind=engine)

        yield

        logger.info("Application shutdown")

    app = FastAPI(
        title=settings.api_name,
        description="TP ",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(auth.router)
    app.include_router(public.router)
    app.include_router(private_user.router)
    app.include_router(private_players.router)
    app.include_router(private_team.router)
    app.include_router(private_match.router)

    return app


app = create_app()

"""NetPulse API application and its Phase 1 setup contract."""

import hashlib
import os
import secrets
from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from alembic import command
from alembic.config import Config
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, StringConstraints, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Setting, User, UserSession
from app.db.session import create_database_engine, create_session_factory, session_dependency

Username = Annotated[
    str,
    StringConstraints(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$"),
]
Password = Annotated[str, StringConstraints(min_length=12, max_length=128)]

password_hasher = PasswordHasher()
SETUP_COMPLETED_KEY = "setup_completed"


class SetupRequest(BaseModel):
    language: Literal["id", "en"]
    timezone: Annotated[str, StringConstraints(min_length=1, max_length=64)]
    username: Username
    password: Password
    email: Annotated[str | None, StringConstraints(max_length=254)] = None

    @field_validator("timezone")
    @classmethod
    def timezone_must_be_an_iana_identifier(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("must be a valid IANA timezone") from exc
        return value

    @field_validator("email")
    @classmethod
    def normalize_optional_email(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower()
        if not normalized:
            return None
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("must be a valid email address")
        return normalized


class SetupStatusResponse(BaseModel):
    setup_complete: bool


class SetupCompleteResponse(SetupStatusResponse):
    admin: dict[str, str]


class LoginRequest(BaseModel):
    username: Annotated[str, StringConstraints(min_length=1, max_length=64)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=128)]
    remember_me: bool = False


def database_url_or_default(database_url: str | None) -> str:
    if database_url:
        return database_url
    if configured_url := os.environ.get("DATABASE_URL"):
        return configured_url
    return "sqlite:///./data/netpulse.db"


def run_migrations(database_url: str) -> None:
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(config, "head")


def create_app(database_url: str | None = None) -> FastAPI:
    """Create an app backed by a migrated SQLite database."""
    resolved_database_url = database_url_or_default(database_url)
    engine = create_database_engine(resolved_database_url)
    run_migrations(resolved_database_url)
    session_factory = create_session_factory(engine)

    def get_session() -> Generator[Session]:
        yield from session_dependency(session_factory)

    app = FastAPI(
        title="NetPulse API",
        description="Self-hosted network monitoring API.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.get("/healthz", tags=["operations"], include_in_schema=False)
    @app.get("/api/v1/health", tags=["operations"])
    def health() -> dict[str, str]:
        """Return liveness only; this endpoint intentionally does not claim readiness."""
        return {"status": "ok", "service": "netpulse-api"}

    @app.get("/api/v1/ready", tags=["operations"])
    def readiness() -> JSONResponse:
        """Scheduler readiness remains unavailable until the monitoring worker exists."""
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {"database": "ready", "scheduler": "not_started"},
            },
        )

    @app.get("/api/v1/setup", response_model=SetupStatusResponse, tags=["setup"])
    def setup_status(session: Annotated[Session, Depends(get_session)]) -> SetupStatusResponse:
        is_complete = (
            session.scalar(select(Setting.key).where(Setting.key == SETUP_COMPLETED_KEY))
            is not None
        )
        return SetupStatusResponse(setup_complete=is_complete)

    @app.post(
        "/api/v1/setup",
        status_code=201,
        response_model=SetupCompleteResponse,
        tags=["setup"],
    )
    def complete_setup(
        request: SetupRequest, session: Annotated[Session, Depends(get_session)]
    ) -> SetupCompleteResponse | JSONResponse:
        if session.scalar(select(Setting.key).where(Setting.key == SETUP_COMPLETED_KEY)):
            return setup_already_complete_response()

        session.add(
            User(
                username=request.username,
                email=request.email,
                password_hash=password_hasher.hash(request.password),
                role="admin",
            )
        )
        session.add(Setting(key=SETUP_COMPLETED_KEY, value="true"))
        session.add(Setting(key="language", value=request.language))
        session.add(Setting(key="timezone", value=request.timezone))
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return setup_already_complete_response()
        return SetupCompleteResponse(
            setup_complete=True,
            admin={"username": request.username, "role": "admin"},
        )

    @app.post("/api/v1/auth/login", tags=["auth"])
    def login(
        request: LoginRequest, session: Annotated[Session, Depends(get_session)]
    ) -> JSONResponse:
        user = session.scalar(select(User).where(User.username == request.username))
        try:
            password_valid = user is not None and password_hasher.verify(
                user.password_hash, request.password
            )
        except VerificationError:
            password_valid = False
        if not password_valid:
            return invalid_credentials_response()

        assert user is not None
        token = secrets.token_urlsafe(32)
        max_age = 60 * 60 * 24 * (30 if request.remember_me else 1)
        session.add(
            UserSession(
                user_id=user.id,
                token_hash=hashlib.sha256(token.encode()).hexdigest(),
                expires_at=datetime.now(UTC) + timedelta(seconds=max_age),
            )
        )
        session.commit()
        response = JSONResponse({"user": {"username": user.username, "role": user.role}})
        response.set_cookie(
            key="netpulse_session",
            value=token,
            max_age=max_age,
            httponly=True,
            samesite="lax",
            secure=os.environ.get("SECURE_COOKIES", "false").lower() == "true",
        )
        return response

    return app


def setup_already_complete_response() -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "setup_already_complete",
                "message": "Initial setup has already been completed.",
                "details": None,
            }
        },
    )


def invalid_credentials_response() -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "error": {
                "code": "invalid_credentials",
                "message": "Invalid username or password.",
                "details": None,
            }
        },
    )


app = create_app()

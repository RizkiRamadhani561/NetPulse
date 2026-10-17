import asyncio
import sqlite3
from contextlib import closing
from pathlib import Path

import httpx
import pytest
from app.main import create_app, database_url_or_default
from argon2 import PasswordHasher


async def request(
    app: object, method: str, path: str, payload: dict[str, str] | None = None
) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.request(method, path, json=payload)


def test_database_url_uses_explicit_value_then_environment_then_safe_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./configured.db")

    assert database_url_or_default("sqlite:///./explicit.db") == "sqlite:///./explicit.db"
    assert database_url_or_default(None) == "sqlite:///./configured.db"

    monkeypatch.delenv("DATABASE_URL")
    assert database_url_or_default(None) == "sqlite:///./data/netpulse.db"


def test_setup_status_is_incomplete_before_an_admin_exists(tmp_path: Path) -> None:
    app = create_app(f"sqlite:///{tmp_path / 'netpulse.db'}")
    response = asyncio.run(request(app, "GET", "/api/v1/setup"))

    assert response.status_code == 200
    assert response.json() == {"setup_complete": False}


def test_setup_creates_one_admin_without_returning_credentials(tmp_path: Path) -> None:
    database = tmp_path / "netpulse.db"
    password = "CorrectHorseBatteryStaple!42"
    app = create_app(f"sqlite:///{database}")
    response = asyncio.run(
        request(
            app,
            "POST",
            "/api/v1/setup",
            {
                "language": "id",
                "timezone": "Asia/Jakarta",
                "username": "admin",
                "email": "admin@example.test",
                "password": password,
            },
        )
    )

    assert response.status_code == 201
    assert response.json() == {
        "setup_complete": True,
        "admin": {"username": "admin", "role": "admin"},
    }
    assert "password" not in response.text
    assert "hash" not in response.text
    with closing(sqlite3.connect(database)) as connection:
        password_hash = connection.execute(
            "SELECT password_hash FROM users WHERE username = ?", ("admin",)
        ).fetchone()[0]
    assert password_hash != password
    assert PasswordHasher().verify(password_hash, password)


def test_setup_rejects_a_second_admin(tmp_path: Path) -> None:
    app = create_app(f"sqlite:///{tmp_path / 'netpulse.db'}")
    initial_response = asyncio.run(
        request(
            app,
            "POST",
            "/api/v1/setup",
            {
                "language": "id",
                "timezone": "UTC",
                "username": "admin",
                "password": "CorrectHorseBatteryStaple!42",
            },
        )
    )
    assert initial_response.status_code == 201

    response = asyncio.run(
        request(
            app,
            "POST",
            "/api/v1/setup",
            {
                "language": "en",
                "timezone": "UTC",
                "username": "another-admin",
                "password": "CorrectHorseBatteryStaple!42",
            },
        )
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "setup_already_complete"


def test_setup_rejects_invalid_timezone_and_short_password(tmp_path: Path) -> None:
    app = create_app(f"sqlite:///{tmp_path / 'netpulse.db'}")
    response = asyncio.run(
        request(
            app,
            "POST",
            "/api/v1/setup",
            {
                "language": "id",
                "timezone": "Not/A-Timezone",
                "username": "admin",
                "password": "short",
            },
        )
    )

    assert response.status_code == 422
    assert response.json()["detail"]


def test_login_rejects_invalid_credentials_without_username_enumeration(tmp_path: Path) -> None:
    app = create_app(f"sqlite:///{tmp_path / 'netpulse.db'}")
    setup = asyncio.run(
        request(
            app,
            "POST",
            "/api/v1/setup",
            {
                "language": "id",
                "timezone": "UTC",
                "username": "admin",
                "password": "CorrectHorseBatteryStaple!42",
            },
        )
    )
    assert setup.status_code == 201

    unknown = asyncio.run(
        request(app, "POST", "/api/v1/auth/login", {"username": "unknown", "password": "wrong"})
    )
    wrong_password = asyncio.run(
        request(app, "POST", "/api/v1/auth/login", {"username": "admin", "password": "wrong"})
    )

    assert unknown.status_code == wrong_password.status_code == 401
    assert unknown.json() == wrong_password.json()


def test_login_sets_an_http_only_session_cookie(tmp_path: Path) -> None:
    app = create_app(f"sqlite:///{tmp_path / 'netpulse.db'}")
    asyncio.run(
        request(
            app,
            "POST",
            "/api/v1/setup",
            {
                "language": "en",
                "timezone": "UTC",
                "username": "admin",
                "password": "CorrectHorseBatteryStaple!42",
            },
        )
    )

    response = asyncio.run(
        request(
            app,
            "POST",
            "/api/v1/auth/login",
            {"username": "admin", "password": "CorrectHorseBatteryStaple!42", "remember_me": True},
        )
    )

    assert response.status_code == 200
    assert response.json() == {"user": {"username": "admin", "role": "admin"}}
    assert "httponly" in response.headers["set-cookie"].lower()
    assert "samesite=lax" in response.headers["set-cookie"].lower()
    assert "CorrectHorseBatteryStaple" not in response.headers["set-cookie"]

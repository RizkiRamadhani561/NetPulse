"""Run a real Uvicorn loopback smoke test without Docker."""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"


def request(url: str) -> tuple[int, bytes]:
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def main() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]

    base_url = f"http://127.0.0.1:{port}"
    with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as server_log:
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
                "--no-access-log",
            ],
            cwd=BACKEND,
            stdout=server_log,
            stderr=subprocess.STDOUT,
        )
        failures: list[str] = []
        try:
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    failures.append(
                        f"Uvicorn exited before becoming healthy (exit={process.returncode})"
                    )
                    break
                try:
                    status, body = request(f"{base_url}/healthz")
                    if status == 200:
                        payload = json.loads(body)
                        if payload == {"status": "ok", "service": "netpulse-api"}:
                            break
                        failures.append(f"/healthz returned an unexpected payload: {payload!r}")
                        break
                except (TimeoutError, urllib.error.URLError, OSError):
                    pass
                time.sleep(0.25)
            else:
                failures.append("Uvicorn did not become healthy within 20 seconds")

            if not failures:
                status, body = request(f"{base_url}/api/v1/health")
                if status != 200 or json.loads(body) != {
                    "status": "ok",
                    "service": "netpulse-api",
                }:
                    failures.append(f"/api/v1/health unexpected response: HTTP {status} {body!r}")

                status, body = request(f"{base_url}/api/v1/ready")
                ready_payload = json.loads(body)
                if status != 503 or ready_payload != {
                    "status": "not_ready",
                    "checks": {
                        "database": "not_configured",
                        "scheduler": "not_started",
                    },
                }:
                    failures.append(
                        f"/api/v1/ready unexpected response: HTTP {status} {ready_payload!r}"
                    )

                status, body = request(f"{base_url}/openapi.json")
                if status != 200:
                    failures.append(f"/openapi.json expected HTTP 200, got {status}")
                else:
                    schema = json.loads(body)
                    if "/api/v1/health" not in schema.get("paths", {}):
                        failures.append("OpenAPI document does not include /api/v1/health")

        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)

            server_log.seek(0)
            output = server_log.read()

        if failures:
            print("API runtime smoke failed:")
            for failure in failures:
                print(f"- {failure}")
            if output:
                print("Uvicorn output:")
                print(output)
            return 1

        print("API runtime smoke passed: liveness, readiness contract, and OpenAPI over loopback.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

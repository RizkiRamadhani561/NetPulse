"""Dependency-free checks for the NetPulse Phase 0 repository structure."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    ".gitignore",
    ".env.example",
    ".pre-commit-config.yaml",
    "LICENSE",
    "AGENTS.md",
    "CLAUDE.md",
    "docker-compose.yml",
    "backend/app/main.py",
    "backend/pyproject.toml",
    "backend/tests/test_health.py",
    "frontend/package.json",
    "frontend/tsconfig.json",
    "frontend/src/app/page.tsx",
    "frontend/src/app/globals.css",
    "frontend/src/messages/id.json",
    "frontend/src/messages/en.json",
    "docs/spec/INDEX.md",
    "docs/ai/PROJECT_STATE.md",
    "docs/ai/TRACEABILITY.md",
    "scripts/verify.sh",
    "scripts/verify_runner.py",
    "backend/tests/test_foundation_contracts.py",
    "docker-compose.lab.yml",
    "lab/README.md",
    "lab/fixtures/oui-mini.csv",
    "lab/fixtures/snmp/system.snmprec",
    "lab/scenarios/default.yml",
    "frontend/.storybook/main.ts",
    "frontend/.storybook/preview.ts",
    "frontend/src/components/dashboard-shell.stories.tsx",
    ".claude/skills/verify/SKILL.md",
    ".claude/skills/ui-review/SKILL.md",
    ".claude/agents/reviewer.md",
    ".claude/agents/security-auditor.md",
    ".claude/agents/ux-auditor.md",
)
SECRET_NAMES = {
    "SECRET_KEY",
    "ENCRYPTION_KEY",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "OIDC_CLIENT_SECRET",
    "SMTP_PASSWORD",
    "VAPID_PRIVATE_KEY",
    "AI_API_KEY",
}


def parse_env_template(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def check() -> int:
    failures = 0
    warnings = 0

    def ok(message: str) -> None:
        print(f"✅ {message}")

    def fail(message: str) -> None:
        nonlocal failures
        failures += 1
        print(f"❌ {message}")

    def warn(message: str) -> None:
        nonlocal warnings
        warnings += 1
        print(f"⚠️ {message}")

    for relative in REQUIRED_PATHS:
        if (ROOT / relative).is_file():
            ok(f"required file exists: {relative}")
        else:
            fail(f"required file missing: {relative}")

    gitignore_path = ROOT / ".gitignore"
    ignore_text = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    if re.search(r"(?m)^\.env(?:\*|$|\.)", ignore_text) and "!.env.example" in ignore_text:
        ok(".env is ignored and .env.example is explicitly allowed")
    else:
        fail(".gitignore must ignore .env files and allow .env.example")

    env_path = ROOT / ".env.example"
    if env_path.exists():
        env_values = parse_env_template(env_path)
        missing = sorted(SECRET_NAMES - env_values.keys())
        populated = sorted(name for name in SECRET_NAMES if env_values.get(name, ""))
        if missing:
            fail(f"secret variable names absent from .env.example: {', '.join(missing)}")
        elif populated:
            fail(f"secret values must remain blank in .env.example: {', '.join(populated)}")
        else:
            ok("required secret names exist in .env.example and have blank values")

    for rel in (
        "frontend/package.json",
        "frontend/tsconfig.json",
        "frontend/src/messages/id.json",
        "frontend/src/messages/en.json",
    ):
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            parsed_json = json.loads(path.read_text(encoding="utf-8"))
            if rel == "frontend/tsconfig.json":
                if isinstance(parsed_json, dict):
                    compiler_options = parsed_json.get("compilerOptions", {})
                else:
                    compiler_options = {}
                if (
                    not isinstance(compiler_options, dict)
                    or compiler_options.get("jsx") != "react-jsx"
                ):
                    fail("frontend/tsconfig.json must set compilerOptions.jsx to react-jsx")
                else:
                    ok("Next.js automatic JSX runtime is preconfigured")

                includes = parsed_json.get("include", []) if isinstance(parsed_json, dict) else []
                required_type_paths = (
                    ".next/types/**/*.ts",
                    ".next/dev/types/**/*.ts",
                )
                missing_type_paths = (
                    [pattern for pattern in required_type_paths if pattern not in includes]
                    if isinstance(includes, list)
                    else list(required_type_paths)
                )
                if missing_type_paths:
                    fail(
                        "frontend/tsconfig.json must preconfigure Next.js generated type paths: "
                        + ", ".join(missing_type_paths)
                    )
                else:
                    ok("Next.js development and production type paths are preconfigured")
            if rel.endswith(("id.json", "en.json")):
                id_values = json.loads(
                    (ROOT / "frontend/src/messages/id.json").read_text(encoding="utf-8")
                )
                en_values = json.loads(
                    (ROOT / "frontend/src/messages/en.json").read_text(encoding="utf-8")
                )
                if set(id_values) != set(en_values):
                    fail("Indonesian and English message dictionaries do not have matching keys")
                else:
                    ok("Indonesian and English message dictionaries have matching keys")
            else:
                ok(f"valid JSON: {rel}")
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON in {rel}: {exc}")

    compose_path = ROOT / "docker-compose.yml"
    if compose_path.is_file():
        compose_text = compose_path.read_text(encoding="utf-8")
        required_mounts = (
            "./frontend/src:/app/src:ro",
            "./frontend/.storybook:/app/.storybook:ro",
        )
        missing_mounts = [mount for mount in required_mounts if mount not in compose_text]
        has_broad_mount = any(
            line.strip() == "- ./frontend:/app" for line in compose_text.splitlines()
        )
        if missing_mounts or has_broad_mount:
            fail(
                "Compose must mount source directories selectively so Next.js runtime files "
                "remain writable by the non-root container user"
            )
        else:
            ok("Compose keeps generated Next.js runtime files outside the source mount")

    pyproject = ROOT / "backend/pyproject.toml"
    if pyproject.exists():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            if data.get("project", {}).get("requires-python") != ">=3.14,<3.15":
                warn("review Python version range against the dependency lock before shipping")
            else:
                ok("backend pyproject TOML parses")
        except tomllib.TOMLDecodeError as exc:
            fail(f"invalid TOML in backend/pyproject.toml: {exc}")

    frontend_css = ROOT / "frontend/src/app/globals.css"
    if frontend_css.exists():
        css = frontend_css.read_text(encoding="utf-8")
        missing_css_tokens = [
            token
            for token in (
                "--teal:",
                "--surface:",
                "prefers-reduced-motion",
                "focus-visible",
            )
            if token not in css
        ]
        if missing_css_tokens:
            for token in missing_css_tokens:
                fail(f"design/accessibility token missing in CSS: {token}")
        else:
            ok("design tokens, focus styles, and reduced-motion rule are present")

    if not (ROOT / "backend/uv.lock").is_file():
        warn("backend/uv.lock not generated; dependency resolution is not reproducible yet")
    if not (ROOT / "frontend/package-lock.json").is_file():
        warn("frontend/package-lock.json not generated; locked installs are not ready yet")

    print("\nFoundation check summary")
    print(f"  failures: {failures}")
    print(f"  warnings: {warnings}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("quick", "full"), default="quick")
    args = parser.parse_args()
    print(f"NetPulse Phase 0 structural verification ({args.mode})")
    return check()


if __name__ == "__main__":
    sys.exit(main())

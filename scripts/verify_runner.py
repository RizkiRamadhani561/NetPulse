"""Cross-platform NetPulse verification runner.

Full mode checks code, tests, builds, dependency advisories and secrets. Docker
Compose runtime integration is deliberately reserved for the final integration
stage and is executed by the manually dispatched GitHub Actions job.
"""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIB = timezone(timedelta(hours=7), "WIB")


def command_text(command: list[str]) -> str:
    if os.name == "nt":
        return subprocess.list2cmdline(command)
    return shlex.join(command)


class VerificationRunner:
    def __init__(self, mode: str) -> None:
        self.mode = mode
        self.started_at = datetime.now(WIB)
        stamp = self.started_at.strftime("%Y-%m-%d-%H%M%S")
        self.report_dir = ROOT / "docs" / "ai" / "verification" / f"local-{stamp}"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.rows: list[dict[str, str]] = []

    def record(self, name: str, status: str, duration: float, log_path: str, detail: str) -> None:
        self.rows.append(
            {
                "name": name,
                "status": status,
                "duration": f"{duration:.1f}s",
                "log": log_path,
                "detail": detail,
            }
        )

    def run_step(self, name: str, command: list[str], cwd: Path = ROOT) -> bool:
        step_slug = name.lower().replace(" ", "-")
        log_file = self.report_dir / f"{len(self.rows) + 1:02d}-{step_slug}.log"
        relative_log = log_file.relative_to(ROOT).as_posix()
        print(f"\n==> {name}: {command_text(command)}", flush=True)
        print(f"    Log: {relative_log}", flush=True)
        started = time.monotonic()
        try:
            shell = os.name == "nt" and command[0].lower().endswith((".cmd", ".bat"))
            with log_file.open("w", encoding="utf-8") as output:
                process = subprocess.Popen(
                    command if not shell else command_text(command),
                    cwd=str(cwd),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                    shell=shell,
                )
                assert process.stdout is not None
                for line in process.stdout:
                    print(line, end="", flush=True)
                    output.write(line)
                return_code = process.wait()
        except OSError as exc:
            output_text = f"Could not start command: {exc}\n"
            log_file.write_text(output_text, encoding="utf-8")
            print(output_text, end="", flush=True)
            return_code = 127
        duration = time.monotonic() - started
        passed = return_code == 0
        status = "✅ Passed" if passed else "❌ Failed"
        self.record(name, status, duration, relative_log, f"exit code {return_code}")
        print(f"<== {name}: {status} ({duration:.1f}s)", flush=True)
        return passed

    def record_status(self, name: str, status: str, detail: str) -> None:
        self.record(name, status, 0.0, "—", detail)

    def write_report(self, exit_code: int) -> Path:
        ended_at = datetime.now(WIB)
        report = self.report_dir / "REPORT.md"
        rows = [
            "# NetPulse Verification Report",
            "",
            f"- **Mode:** {self.mode}",
            f"- **Started:** {self.started_at.isoformat()}",
            f"- **Finished:** {ended_at.isoformat()}",
            f"- **Repository root:** `{ROOT}`",
            f"- **Exit code:** {exit_code}",
            "",
            "| Check | Status | Duration | Evidence | Detail |",
            "|---|---|---:|---|---|",
        ]
        for row in self.rows:
            rows.append(
                f"| {row['name']} | {row['status']} | {row['duration']} | "
                f"`{row['log']}` | {row['detail']} |"
            )
        rows.extend(
            [
                "",
                "## Container integration",
                "",
                (
                    "Docker Compose runtime smoke is intentionally deferred to the final "
                    "integration stage. Run the repository CI workflow manually after feature "
                    "work and regular checks are stable. This is a deferral, not a passing result."
                ),
                "",
            ]
        )
        report.write_text("\n".join(rows), encoding="utf-8")
        return report

    def run(self) -> int:
        python = sys.executable
        structure_ok = self.run_step(
            "Structure and safety contracts",
            [python, "scripts/verify_project.py", "--mode", self.mode],
        )
        if not structure_ok:
            report = self.write_report(1)
            print(f"\nVerification failed. Report: {report.relative_to(ROOT)}")
            return 1

        if self.mode == "full":
            uv = "uv"
            npm = "npm.cmd" if os.name == "nt" else "npm"
            gitleaks = "gitleaks"
            missing = [
                tool
                for label, tool in (("uv", uv), ("npm", npm), ("gitleaks", gitleaks))
                if shutil.which(tool) is None
            ]
            missing_lockfiles = [
                path
                for path in ("backend/uv.lock", "frontend/package-lock.json")
                if not (ROOT / path).is_file()
            ]
            if missing or missing_lockfiles:
                detail = []
                if missing:
                    detail.append("missing tools: " + ", ".join(missing))
                if missing_lockfiles:
                    detail.append("missing lockfiles: " + ", ".join(missing_lockfiles))
                self.record_status("Full-verification preflight", "❌ Failed", "; ".join(detail))
                report = self.write_report(1)
                print(f"\nVerification failed. Report: {report.relative_to(ROOT)}")
                return 1

            backend_ok = self.run_step(
                "Backend locked dependency sync",
                [uv, "sync", "--locked", "--extra", "dev"],
                ROOT / "backend",
            )
            if backend_ok:
                backend_checks = [
                    (
                        "Ruff lint",
                        [
                            uv,
                            "run",
                            "--locked",
                            "--extra",
                            "dev",
                            "ruff",
                            "check",
                            "app",
                            "tests",
                            "../scripts",
                        ],
                    ),
                    (
                        "Ruff format",
                        [
                            uv,
                            "run",
                            "--locked",
                            "--extra",
                            "dev",
                            "ruff",
                            "format",
                            "--check",
                            "app",
                            "tests",
                            "../scripts",
                        ],
                    ),
                    ("Mypy", [uv, "run", "--locked", "--extra", "dev", "mypy", "app"]),
                    (
                        "Backend tests and coverage",
                        [
                            uv,
                            "run",
                            "--locked",
                            "--extra",
                            "dev",
                            "pytest",
                            "tests",
                            "-q",
                            "--cov=app",
                            "--cov-report=term-missing",
                            "--cov-fail-under=70",
                        ],
                    ),
                    (
                        "Backend dependency audit",
                        [uv, "run", "--locked", "--extra", "dev", "pip-audit"],
                    ),
                ]
                for name, command in backend_checks:
                    if not self.run_step(name, command, ROOT / "backend"):
                        # Continue independent checks to collect all useful evidence.
                        pass
            else:
                for name in (
                    "Ruff lint",
                    "Ruff format",
                    "Mypy",
                    "Backend tests and coverage",
                    "Backend dependency audit",
                ):
                    self.record_status(name, "⏭️ Skipped", "backend dependency sync failed")

            frontend_ok = self.run_step(
                "Frontend locked dependency install",
                [npm, "ci", "--no-audit", "--no-fund"],
                ROOT / "frontend",
            )
            if frontend_ok:
                frontend_checks = [
                    ("Frontend typecheck", [npm, "run", "typecheck"]),
                    ("Frontend production build", [npm, "run", "build"]),
                    ("Storybook build", [npm, "run", "build-storybook"]),
                    ("Frontend dependency audit", [npm, "audit", "--audit-level=high"]),
                ]
                for name, command in frontend_checks:
                    if not self.run_step(name, command, ROOT / "frontend"):
                        pass
            else:
                for name in (
                    "Frontend typecheck",
                    "Frontend production build",
                    "Storybook build",
                    "Frontend dependency audit",
                ):
                    self.record_status(name, "⏭️ Skipped", "npm ci failed")

            self.run_step("Secret scan", [gitleaks, "dir", "--redact", "."], ROOT)

        failures = [row for row in self.rows if row["status"] == "❌ Failed"]
        exit_code = 1 if failures else 0
        report = self.write_report(exit_code)
        print("\nVerification summary")
        print("| Check | Status | Duration |")
        print("|---|---|---:|")
        for row in self.rows:
            print(f"| {row['name']} | {row['status']} | {row['duration']} |")
        print(f"\nReport saved to: {report.relative_to(ROOT)}")
        if exit_code:
            print("❌ One or more verification checks failed.")
        else:
            print(
                "✅ All applicable non-container checks passed. "
                "Docker integration remains deferred."
            )
        return exit_code


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("quick", "full"), default="quick")
    args = parser.parse_args()
    return VerificationRunner(args.mode).run()


if __name__ == "__main__":
    raise SystemExit(main())

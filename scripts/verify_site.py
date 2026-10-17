from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


REQUIRED_FILES = (
    "index.html",
    "docs.html",
    "styles.css",
    "site.js",
    "robots.txt",
    "sitemap.xml",
    "assets/brand/netpulse-mark.svg",
    "assets/brand/netpulse-mark-alt.svg",
    "assets/brand/netpulse-logo.svg",
    "assets/brand/favicon.svg",
    "assets/brand/github-banner.svg",
    "assets/brand/login-background.svg",
    "assets/brand/topology-pattern.svg",
)
CANVA_REFERENCE = re.compile(r"canva\.com|media\.canva\.com", re.IGNORECASE)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.ids: list[str] = []
        self.translation_keys: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attr in ("src", "href"):
            value = values.get(attr)
            if value:
                self.references.append(value)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
        translation_key = values.get("data-i18n")
        if translation_key:
            self.translation_keys.append(translation_key)


def resolve_local_reference(root: Path, ref: str, source: Path) -> Path | None:
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    target_path = parsed.path
    if target_path in (".", "./", ""):
        target_path = "index.html"
    candidate = (source.parent / target_path).resolve()
    resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValueError(f"Reference escapes site root: {ref} from {source.relative_to(root)}")
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate NetPulse's static GitHub Pages artifact."
    )
    parser.add_argument("--root", type=Path, required=True, help="Root of assembled site artifact")
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    for name in REQUIRED_FILES:
        path = root / name
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty required file: {name}")

    html_files = [root / "index.html", root / "docs.html"]
    translation_keys: set[str] = set()
    for html_path in html_files:
        if not html_path.is_file():
            continue
        page = PageParser()
        try:
            page.feed(html_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"Cannot read {html_path.name}: {exc}")
            continue
        seen: set[str] = set()
        for element_id in page.ids:
            if element_id in seen:
                errors.append(f"Duplicate id #{element_id} in {html_path.name}")
            seen.add(element_id)
        translation_keys.update(page.translation_keys)
        for ref in page.references:
            try:
                target = resolve_local_reference(root, ref, html_path)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if target is not None and not target.is_file():
                errors.append(f"Broken local reference in {html_path.name}: {ref}")

    js_path = root / "site.js"
    if js_path.is_file():
        js = js_path.read_text(encoding="utf-8")
        for key in sorted(translation_keys):
            if not re.search(r"\b" + re.escape(key) + r"\s*:", js):
                errors.append(f"Missing translation key in site.js: {key}")

    css_path = root / "styles.css"
    if css_path.is_file():
        css = css_path.read_text(encoding="utf-8")
        for raw in re.findall(r"url\(\s*['\"]?([^'\")]+)", css):
            ref = raw.strip()
            if ref.startswith(("data:", "http:", "https:", "#")):
                continue
            candidate = (css_path.parent / ref).resolve()
            if root not in candidate.parents and candidate != root:
                errors.append(f"CSS reference escapes site root: {ref}")
            elif not candidate.is_file():
                errors.append(f"Broken CSS reference: {ref}")

    for svg_path in root.rglob("*.svg"):
        try:
            ET.parse(svg_path)
        except (ET.ParseError, OSError) as exc:
            errors.append(f"Invalid SVG {svg_path.relative_to(root)}: {exc}")

    source_suffixes = {".html", ".css", ".js", ".xml", ".txt", ".svg"}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in source_suffixes:
            text = path.read_text(encoding="utf-8", errors="replace")
            if CANVA_REFERENCE.search(text):
                relative_path = path.relative_to(root)
                errors.append(
                    f"External Canva or expiring thumbnail reference found in {relative_path}"
                )

    sitemap = root / "sitemap.xml"
    if sitemap.is_file():
        try:
            ET.parse(sitemap)
        except ET.ParseError as exc:
            errors.append(f"Invalid sitemap.xml: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Site validation failed with {len(errors)} issue(s).", file=sys.stderr)
        return 1
    print(
        f"Site validation passed: {len(REQUIRED_FILES)} required files, local links, "
        "translations, and SVG/XML syntax."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

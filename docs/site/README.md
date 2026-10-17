# NetPulse public site

This directory contains a dependency-free project landing page and a short technical documentation overview. The files use local HTML, CSS, JavaScript, and repository-owned SVG assets; no external font CDN, tracking service, or third-party JavaScript is required.

## Preview locally

Run the following from the repository root in Windows PowerShell:

    $preview = Join-Path $PWD "site-preview"
    New-Item -ItemType Directory -Force -Path "$preview/assets/brand" | Out-Null
    Copy-Item "docs/site/*" $preview -Recurse -Force
    Copy-Item "frontend/public/brand/*" "$preview/assets/brand" -Force
    python -m http.server 8001 --directory $preview

Then open http://localhost:8001. The temporary preview folder is generated locally and is not tracked by Git. The site uses relative asset paths so it can run at the repository's GitHub Pages project URL as well as on localhost.

## Publish with GitHub Pages

The workflow at .github/workflows/pages.yml assembles the site and canonical vector assets, then uploads the deploy artifact to GitHub Pages. It runs on changes merged to main or by manual dispatch. It does not publish the Next.js app itself: GitHub Pages hosts only this static project site and docs overview.

On a push to main or a manual workflow dispatch, the workflow uses the official configure-pages action with its enablement option to request GitHub Pages setup automatically. Pull requests only assemble and validate the site; they do not publish it. If repository policy, plan restrictions, or token permissions prevent automatic enablement, a repository administrator must open **Settings → Pages**, choose **GitHub Actions** under **Build and deployment → Source**, and rerun the workflow. After deployment succeeds, check the Actions run summary and the repository Pages environment for the published URL.

Expected URL: https://rizkiramadhani561.github.io/NetPulse/

## Content policy

Public copy distinguishes the current Phase 0 foundation from planned work. Do not claim login, real device monitoring, SNMP polling, alert delivery, or production readiness until implementation and verification evidence support those claims. This site is a project overview; it is not the product's login screen.

## File map

- index.html — project landing page.
- docs.html — status, local setup, verification notes, security boundaries, and source references.
- styles.css — shared responsive design system, dark/light theme tokens, and mobile rules.
- site.js — language/theme toggles. Preference storage is optional and guarded.
- assets/brand/ — copied from frontend/public/brand during the Pages build.
- scripts/verify_site.py — checks required assets, local references, translation keys, SVG/XML syntax, and accidental Canva preview URLs in CI.

# NetPulse brand guidelines

Last updated: 2026-10-17

## Direction

NetPulse has a quiet infrastructure-tool identity: ink navy, restrained teal, a simple pulse trace, cool-slate topology lines, consistent line weights, and generous negative space. The interface is a monitoring workspace, so branding must never compete with alerts, labels, or data.

Avoid neon glow, chrome or metallic effects, fake glass, heavy gradients, overdrawn circuit boards, random hexagons, decorative dashboards, and motion that distracts from operational work.

## Palette

| Token | Hex | Intended use |
|---|---|---|
| Ink navy | #0B1220 | Background artwork and site surfaces |
| Deep navy | #111827 | Logo tile and dark interface accents |
| Teal | #14B8A6 | Pulse trace, key accents, interactive focus |
| Cool blue | #38BDF8 | Alternate topology mark only, used sparingly |
| Off-white | #F8FAFC | Clear details on dark surfaces |
| Slate | #334155 / #64748B | Grids, routes, secondary lines |

The existing application shell keeps its established dark surface tokens; its teal accent has been aligned with the primary brand teal. Keep contrast and existing layout hierarchy intact instead of repainting every dashboard surface just to force a perfect match.

## Canonical asset inventory

All web-app assets live under frontend/public/brand/. The GitHub Pages workflow copies the same directory to the published artifact at assets/brand/, so the site does not depend on temporary Canva URLs.

| Asset | Use |
|---|---|
| netpulse-mark.svg | Primary square mark; sidebar and compact brand placements |
| netpulse-mark-alt.svg | Alternate topology mark for secondary surfaces, not a competing primary logo |
| netpulse-logo.svg | Horizontal wordmark for the site header and external documentation |
| favicon.svg | Browser tab icon for the app and public site |
| github-banner.svg | Repository README banner and landing-page illustration |
| login-background.svg | Prepared background artwork for a future authentication route |
| topology-pattern.svg | Optional subtle background for supporting surfaces |

## Usage rules

1. Prefer SVG for logos, icons, and simple diagrams. It stays sharp on high-density screens and avoids redundant raster files.
2. Use the primary mark at small sizes. Avoid using the full wordmark in tiny spaces where its subtitle would become illegible.
3. If “NetPulse” already appears adjacent to a mark, the image alt text may be empty; a standalone linked logo needs a meaningful accessible name.
4. Keep focus rings visible and text contrast strong. Do not place the white wordmark directly on a light panel without a suitable alternate variant.
5. Use the login background as decoration only. The login form, errors, labels, password controls, and all interactive states must remain accessible HTML/React, not pixels baked into a background.
6. Do not create a login route with a fake form until authentication is implemented and tested. Current Phase 0 does not include production authentication.
7. Use local repository assets rather than signed CDN thumbnails. Optimized WebP can be appropriate for future photographic screenshots, but vector marks should remain SVG unless a consumer specifically requires PNG/ICO.
8. Do not label mockups as live monitoring. Product claims must follow the current README, project state, tests, and release gates.

## Canva concept references and provenance

Six generated image concepts were found in the connected Canva library during the brand pass. Their media IDs are:

- MAHYP7ODm1k
- MAHYP9xP1Jk
- MAHYP6VTeR0
- MAHYP_BoSNE
- MAHYP7S69JI
- MAHYP7n_7gY

The connector returned asset metadata and small watermarked thumbnails, but did not expose downloadable full-resolution image bytes. The temporary thumbnail URLs were signed and expire; they were not committed. The SVG files in this repository are hand-authored vector assets following the requested design direction, not byte-for-byte exports of those Canva generations. Should the original licensed exports be obtained later, they can be reviewed and deliberately replace or complement these files, without introducing watermarks or expiring runtime dependencies.

## Review checklist for future design changes

- [ ] Sidebar mark is readable at compact sizes.
- [ ] Banner and login art do not obscure headlines or form controls.
- [ ] Primary and secondary text pass contrast checks in both themes.
- [ ] Mobile navigation does not overflow or hide language/theme controls.
- [ ] Reduced-motion settings are honored.
- [ ] Every interactive element works with a keyboard and has a visible focus state.
- [ ] Screenshots and claims accurately distinguish implemented UI from planned product functionality.

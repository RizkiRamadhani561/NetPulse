"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawn } = require("node:child_process");
const { chromium } = require("playwright");
const AxeBuilder = require("@axe-core/playwright").default;

const ROOT = path.resolve(__dirname, "..");
const FRONTEND = path.join(ROOT, "frontend");
const ARTIFACTS =
  process.env.NETPULSE_UI_ARTIFACTS || path.join(os.tmpdir(), "netpulse-ui-artifacts");
const BASE_URL = process.env.NETPULSE_UI_BASE_URL || "http://127.0.0.1:3100";
const failures = [];
const auditResults = [];
const runtimeErrors = [];
let server;
let serverOutput = "";

function check(condition, message) {
  if (!condition) failures.push(message);
}

function captureServerOutput(chunk) {
  serverOutput = (serverOutput + chunk.toString()).slice(-12000);
}

async function waitForServer(url, attempts = 60) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(2000) });
      if (response.ok) return;
    } catch {
      // The production server takes a moment to bind the local port.
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error(`Next.js did not become healthy at ${url}.\n${serverOutput}`);
}

async function assertNoHorizontalOverflow(page, widthLabel) {
  const result = await page.evaluate(() => ({
    viewport: window.innerWidth,
    document: document.documentElement.scrollWidth,
    body: document.body.scrollWidth,
  }));
  check(
    result.document <= result.viewport && result.body <= result.viewport,
    `${widthLabel}: horizontal overflow (viewport=${result.viewport}, document=${result.document}, body=${result.body})`,
  );
}

async function runAxe(page, label) {
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22a", "wcag22aa"])
    .analyze();
  auditResults.push({
    label,
    passes: result.passes.length,
    incomplete: result.incomplete.map((item) => ({ id: item.id, impact: item.impact })),
    violations: result.violations.map((item) => ({
      id: item.id,
      impact: item.impact,
      help: item.help,
      helpUrl: item.helpUrl,
      nodes: item.nodes.map((node) => ({
        target: node.target,
        summary: node.failureSummary,
      })),
    })),
  });
  for (const violation of result.violations) {
    failures.push(
      `${label}: axe ${violation.impact || "unknown"} violation ${violation.id} — ${violation.help} (${violation.nodes.length} node(s))`,
    );
  }
}

async function main() {
  fs.mkdirSync(ARTIFACTS, { recursive: true });
  const npm = process.platform === "win32" ? "npm.cmd" : "npm";
  server = spawn(
    npm,
    ["run", "start", "--", "--hostname", "127.0.0.1", "--port", "3100"],
    {
      cwd: FRONTEND,
      env: { ...process.env, NEXT_TELEMETRY_DISABLED: "1", NODE_ENV: "production" },
      shell: process.platform === "win32",
      stdio: ["ignore", "pipe", "pipe"],
    },
  );
  server.stdout?.on("data", captureServerOutput);
  server.stderr?.on("data", captureServerOutput);
  server.on("error", (error) => runtimeErrors.push(`server error: ${error.message}`));

  let browser;
  try {
    await waitForServer(BASE_URL);
    browser = await chromium.launch({ headless: true });

    const desktop = await browser.newPage({
      viewport: { width: 1440, height: 900 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    desktop.on("console", (message) => {
      if (message.type() === "error") runtimeErrors.push(`console: ${message.text()}`);
    });
    desktop.on("pageerror", (error) => runtimeErrors.push(`pageerror: ${error.message}`));
    desktop.on("requestfailed", (request) => {
      runtimeErrors.push(`request failed: ${request.url()} — ${request.failure()?.errorText || "unknown"}`);
    });
    desktop.on("response", (response) => {
      if (response.status() >= 400 && !response.url().endsWith("/favicon.ico")) {
        runtimeErrors.push(`HTTP ${response.status()}: ${response.url()}`);
      }
    });

    const response = await desktop.goto(BASE_URL, { waitUntil: "networkidle", timeout: 30000 });
    check(response?.status() === 200, `desktop home page expected HTTP 200, got ${response?.status()}`);
    check(await desktop.locator("main h1").isVisible(), "desktop: main h1 is missing or hidden");
    check((await desktop.locator(".metric-card__value").allTextContents()).every((value) => value.trim() === "—"),
      "foundation preview must not display fabricated monitoring metric values");
    await assertNoHorizontalOverflow(desktop, "desktop 1440px");
    await desktop.screenshot({
      path: path.join(ARTIFACTS, "dashboard-desktop-id.png"),
      fullPage: true,
      animations: "disabled",
    });
    await runAxe(desktop, "desktop-id");

    const langButton = desktop.locator(".language-toggle");
    check(await langButton.count() === 1, "language toggle must exist exactly once");
    await langButton.click();
    await desktop.waitForFunction(() => document.documentElement.lang === "en", null, { timeout: 3000 });
    check((await desktop.locator("main h1").innerText()).trim().length > 0,
      "English locale left the page title empty");
    await desktop.screenshot({
      path: path.join(ARTIFACTS, "dashboard-desktop-en.png"),
      fullPage: true,
      animations: "disabled",
    });
    await runAxe(desktop, "desktop-en");

    const keyboardPage = await browser.newPage({ viewport: { width: 1024, height: 768 } });
    keyboardPage.on("console", (message) => {
      if (message.type() === "error") runtimeErrors.push(`keyboard console: ${message.text()}`);
    });
    await keyboardPage.goto(BASE_URL, { waitUntil: "networkidle" });
    await keyboardPage.keyboard.press("Tab");
    const firstFocus = await keyboardPage.evaluate(() => {
      const active = document.activeElement;
      const style = active ? getComputedStyle(active) : null;
      return {
        tag: active?.tagName || "",
        name: active?.getAttribute("aria-label") || active?.textContent?.trim() || "",
        outlineStyle: style?.outlineStyle || "none",
        outlineWidth: style?.outlineWidth || "0px",
        boxShadow: style?.boxShadow || "none",
      };
    });
    check(firstFocus.tag === "A" || firstFocus.tag === "BUTTON",
      `keyboard: first Tab did not focus an interactive control (${firstFocus.tag})`);
    check(
      (firstFocus.outlineStyle !== "none" && firstFocus.outlineWidth !== "0px") ||
        firstFocus.boxShadow !== "none",
      `keyboard: first focused control has no visible focus treatment (${JSON.stringify(firstFocus)})`,
    );
    let languageReached = false;
    for (let i = 0; i < 24; i += 1) {
      const onLanguageButton = await keyboardPage.evaluate(() =>
        document.activeElement?.classList.contains("language-toggle") === true,
      );
      if (onLanguageButton) {
        languageReached = true;
        break;
      }
      await keyboardPage.keyboard.press("Tab");
    }
    check(languageReached, "keyboard: language toggle is not reachable with Tab");
    if (languageReached) {
      await keyboardPage.keyboard.press("Enter");
      await keyboardPage.waitForFunction(() => document.documentElement.lang === "en", null, { timeout: 3000 });
    }

    for (const width of [390, 360]) {
      const mobile = await browser.newPage({
        viewport: { width, height: 844 },
        deviceScaleFactor: 1,
        isMobile: true,
        hasTouch: true,
        reducedMotion: "reduce",
      });
      mobile.on("console", (message) => {
        if (message.type() === "error") runtimeErrors.push(`mobile ${width} console: ${message.text()}`);
      });
      mobile.on("pageerror", (error) => runtimeErrors.push(`mobile ${width} pageerror: ${error.message}`));
      await mobile.goto(BASE_URL, { waitUntil: "networkidle", timeout: 30000 });
      check(await mobile.locator("main h1").isVisible(), `mobile ${width}px: main h1 is missing or hidden`);
      await assertNoHorizontalOverflow(mobile, `mobile ${width}px`);
      if (width === 390) {
        await mobile.screenshot({
          path: path.join(ARTIFACTS, "dashboard-mobile-390.png"),
          fullPage: true,
          animations: "disabled",
        });
        await runAxe(mobile, "mobile-390-id");
      } else {
        await mobile.screenshot({
          path: path.join(ARTIFACTS, "dashboard-mobile-360.png"),
          fullPage: true,
          animations: "disabled",
        });
      }
      await mobile.close();
    }
    await keyboardPage.close();
    await desktop.close();
  } finally {
    if (browser) await browser.close().catch(() => undefined);
    if (server && server.exitCode === null) {
      server.kill("SIGTERM");
      await new Promise((resolve) => {
        const timer = setTimeout(resolve, 3000);
        server.once("exit", () => {
          clearTimeout(timer);
          resolve();
        });
      });
      if (server.exitCode === null) server.kill("SIGKILL");
    }
    fs.writeFileSync(
      path.join(ARTIFACTS, "ui-audit-summary.json"),
      JSON.stringify({ failures, runtimeErrors, auditResults }, null, 2) + "\n",
    );
  }
  if (runtimeErrors.length) {
    for (const error of runtimeErrors) failures.push(error);
  }
  if (failures.length) {
    console.error("Phase 0 UI audit failed:");
    for (const failure of failures) console.error(`- ${failure}`);
    console.error(`Artifacts: ${ARTIFACTS}`);
    if (serverOutput) console.error(`Next.js output:\n${serverOutput}`);
    process.exitCode = 1;
  } else {
    console.log("Phase 0 UI audit passed.");
    console.log(`Axe audits: ${auditResults.length}; screenshots and JSON report: ${ARTIFACTS}`);
  }
}

main().catch((error) => {
  console.error(error.stack || error);
  if (serverOutput) console.error(`Next.js output:\n${serverOutput}`);
  process.exitCode = 1;
});

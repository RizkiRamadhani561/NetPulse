"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { createRequire } = require("node:module");
const { spawn } = require("node:child_process");

const ROOT = path.resolve(__dirname, "..");
const FRONTEND = path.join(ROOT, "frontend");
const frontendRequire = createRequire(path.join(FRONTEND, "package.json"));
const { chromium } = frontendRequire("playwright");
const AxeBuilder = frontendRequire("@axe-core/playwright").default;
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

function captureConsoleError(label, message) {
  const text = message.text();
  if (text === "Failed to load resource: the server responded with a status of 404 (Not Found)" ||
      text === "Failed to load resource: the server responded with a status of 503 (Service Unavailable)") return;
  runtimeErrors.push(`${label}: ${text}`);
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
  const nextCli = path.join(FRONTEND, "node_modules", "next", "dist", "bin", "next");
  server = spawn(
    process.execPath,
    [nextCli, "start", "--hostname", "127.0.0.1", "--port", "3100"],
    {
      cwd: FRONTEND,
      env: { ...process.env, NEXT_TELEMETRY_DISABLED: "1", NODE_ENV: "production" },
      stdio: ["ignore", "pipe", "pipe"],
    },
  );
  server.stdout?.on("data", captureServerOutput);
  server.stderr?.on("data", captureServerOutput);
  server.on("error", (error) => runtimeErrors.push(`server error: ${error.message}`));

  let browser;
  try {
    await waitForServer(BASE_URL);
    browser = await chromium.launch({
      headless: true,
      executablePath: process.env.NETPULSE_CHROMIUM_EXECUTABLE,
    });

    const desktopContext = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    const desktop = await desktopContext.newPage();
    desktop.on("console", (message) => {
      if (message.type() === "error") captureConsoleError("console", message);
    });
    desktop.on("pageerror", (error) => runtimeErrors.push(`pageerror: ${error.message}`));
    desktop.on("requestfailed", (request) => {
      runtimeErrors.push(`request failed: ${request.url()} — ${request.failure()?.errorText || "unknown"}`);
    });
    desktop.on("response", (response) => {
      const expectedSetupUnavailability = response.url().endsWith("/api/setup") && response.status() === 503;
      if (response.status() >= 400 && !response.url().endsWith("/favicon.ico") && !expectedSetupUnavailability) {
        runtimeErrors.push(`HTTP ${response.status()}: ${response.url()}`);
      }
    });

    const response = await desktop.goto(BASE_URL, { waitUntil: "networkidle", timeout: 30000 });
    check(response?.status() === 200, `desktop home page expected HTTP 200, got ${response?.status()}`);
    check(await desktop.locator("main h1").isVisible(), "desktop: main h1 is missing or hidden");
    await desktop.locator(".setup-error").waitFor({ state: "visible", timeout: 10000 });
    check(await desktop.locator(".setup-error").isVisible(), "desktop: setup API error state is missing");
    check(await desktop.locator(".setup-error button").isVisible(), "desktop: setup retry action is missing");
    await assertNoHorizontalOverflow(desktop, "desktop 1440px");
    await desktop.screenshot({
      path: path.join(ARTIFACTS, "dashboard-desktop-id.png"),
      fullPage: true,
      animations: "disabled",
    });
    await runAxe(desktop, "desktop-id");

    const keyboardContext = await browser.newContext({ viewport: { width: 1024, height: 768 } });
    const keyboardPage = await keyboardContext.newPage();
    keyboardPage.on("console", (message) => {
      if (message.type() === "error") captureConsoleError("keyboard console", message);
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
    let retryReached = false;
    for (let i = 0; i < 24; i += 1) {
      const onRetryButton = await keyboardPage.evaluate(() =>
        document.activeElement?.textContent?.trim() === "Coba lagi",
      );
      if (onRetryButton) {
        retryReached = true;
        break;
      }
      await keyboardPage.keyboard.press("Tab");
    }
    check(retryReached, "keyboard: setup retry action is not reachable with Tab");

    for (const width of [390, 360]) {
      const mobileContext = await browser.newContext({
        viewport: { width, height: 844 },
        deviceScaleFactor: 1,
        isMobile: true,
        hasTouch: true,
        reducedMotion: "reduce",
      });
      const mobile = await mobileContext.newPage();
      mobile.on("console", (message) => {
        if (message.type() === "error") captureConsoleError(`mobile ${width} console`, message);
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
      await mobileContext.close();
    }
    await keyboardContext.close();
    await desktopContext.close();
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

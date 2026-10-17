"use client";

import { useEffect, useState } from "react";
import en from "@/messages/en.json";
import id from "@/messages/id.json";

type Language = "id" | "en";
type Copy = Record<string, string>;

const messages: Record<Language, Copy> = { id, en };

function PulseMark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <img src="/brand/netpulse-mark.svg" width={35} height={35} alt="" />
    </span>
  );
}

function TinyArrow() {
  return (
    <svg aria-hidden="true" viewBox="0 0 16 16" fill="none" className="tiny-arrow">
      <path d="M3 8h9M8 3l5 5-5 5" />
    </svg>
  );
}

function MetricCard({ label, value, note, icon }: { label: string; value: string; note: string; icon: string }) {
  return (
    <article className="metric-card">
      <div className="metric-card__top">
        <span className="metric-card__label">{label}</span>
        <span className="metric-card__icon" aria-hidden="true">{icon}</span>
      </div>
      <p className="metric-card__value">{value}</p>
      <p className="metric-card__note">{note}</p>
    </article>
  );
}

export function DashboardShell() {
  const [language, setLanguage] = useState<Language>("id");
  const copy = messages[language];

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  return (
    <div className="app-shell" id="overview">
      <aside className="sidebar" aria-label={copy.primaryNavigation}>
        <a className="brand" href="#overview" aria-label="NetPulse home">
          <PulseMark />
          <span className="brand-copy">
            <strong>NetPulse</strong>
            <small>NETWORK OBSERVABILITY</small>
          </span>
        </a>

        <div className="workspace-switcher">
          <span className="workspace-avatar">N</span>
          <span className="workspace-copy"><strong>{copy.workspace}</strong><small>{copy.localWorkspace}</small></span>
          <span className="switcher-chevron" aria-hidden="true">⌄</span>
        </div>

        <p className="sidebar-label">{copy.workspaceSection}</p>
        <nav className="main-nav" aria-label={copy.primaryNavigation}>
          <a className="nav-item nav-item--active" href="#overview" aria-current="page">
            <span className="nav-glyph nav-glyph--pulse" aria-hidden="true">⌁</span><span>{copy.overview}</span><span className="nav-count">01</span>
          </a>
          <button className="nav-item" type="button" disabled aria-disabled="true">
            <span className="nav-glyph" aria-hidden="true">▦</span><span>{copy.devices}</span><span className="nav-planned">{copy.planned}</span>
          </button>
          <button className="nav-item" type="button" disabled aria-disabled="true">
            <span className="nav-glyph" aria-hidden="true">⌘</span><span>{copy.discovery}</span><span className="nav-planned">{copy.planned}</span>
          </button>
          <button className="nav-item" type="button" disabled aria-disabled="true">
            <span className="nav-glyph" aria-hidden="true">◎</span><span>{copy.alerts}</span><span className="nav-planned">{copy.planned}</span>
          </button>
          <button className="nav-item" type="button" disabled aria-disabled="true">
            <span className="nav-glyph" aria-hidden="true">▤</span><span>{copy.reports}</span><span className="nav-planned">{copy.planned}</span>
          </button>
        </nav>

        <div className="sidebar-spacer" />
        <div className="sidebar-safety">
          <span className="safety-icon" aria-hidden="true">⌑</span>
          <div><strong>{copy.safeByDefault}</strong><p>{copy.safeByDefaultNote}</p></div>
        </div>
        <div className="sidebar-footer"><span className="online-dot" />{copy.localPreview}<span className="version-label">v0.1.0</span></div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div className="breadcrumb"><span>{copy.workspace}</span><span className="breadcrumb-slash">/</span><strong>{copy.overview}</strong></div>
          <div className="topbar-actions">
            <span className="environment-pill"><span className="environment-dot" />{copy.foundationPreview}</span>
            <span className="topbar-divider" />
            <button className="language-toggle" type="button" onClick={() => setLanguage(language === "id" ? "en" : "id")} aria-label={copy.switchLanguage}>
              <span className="language-icon" aria-hidden="true">文</span>{language === "id" ? "ID" : "EN"}<span className="switcher-chevron" aria-hidden="true">⌄</span>
            </button>
            <div className="avatar" aria-label={copy.localPreview} title={copy.localPreview}>N</div>
          </div>
        </header>

        <div className="content-wrap">
          <section className="welcome-row" aria-labelledby="page-title">
            <div>
              <p className="eyebrow"><span className="eyebrow-line" />{copy.overviewEyebrow}</p>
              <h1 id="page-title">{copy.pageTitle}<span className="title-period">.</span></h1>
              <p className="page-subtitle">{copy.pageSubtitle}</p>
            </div>
            <div className="welcome-date"><span className="date-icon" aria-hidden="true">◷</span><span>{copy.localOnly}</span></div>
          </section>

          <section className="metrics-grid" aria-label={copy.metricsSection}>
            <MetricCard label={copy.monitoredDevices} value="—" note={copy.availablePhaseOne} icon="⌗" />
            <MetricCard label={copy.overallUptime} value="—" note={copy.awaitingSamples} icon="◷" />
            <MetricCard label={copy.averageLatency} value="—" note={copy.awaitingChecks} icon="↗" />
            <MetricCard label={copy.openIncidents} value="—" note={copy.awaitingIncidents} icon="◎" />
          </section>

          <section className="content-grid">
            <article className="panel panel--wide">
              <div className="panel-heading">
                <div><p className="section-kicker">01 / {copy.networkHealth}</p><h2>{copy.activityTitle}</h2><p className="panel-caption">{copy.activitySubtitle}</p></div>
                <span className="period-chip">{copy.last24Hours}<span aria-hidden="true">⌄</span></span>
              </div>
              <div className="empty-graph" role="img" aria-label={copy.emptyGraphLabel}>
                <div className="graph-gridline graph-gridline--one" /><div className="graph-gridline graph-gridline--two" /><div className="graph-gridline graph-gridline--three" />
                <div className="graph-empty-state"><span className="graph-icon" aria-hidden="true"><svg viewBox="0 0 40 40" fill="none"><path d="M4 22h8l4-10 7 18 5-13 3 5h5" /><circle cx="20" cy="20" r="17.5" /></svg></span><strong>{copy.noMonitoringData}</strong><span>{copy.noMonitoringDataNote}</span></div>
                <div className="graph-axis"><span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span></div>
              </div>
              <div className="panel-bottom-note"><span className="neutral-dot" />{copy.graphFooter}</div>
            </article>

            <article className="panel setup-panel">
              <div className="panel-heading panel-heading--compact"><div><p className="section-kicker">02 / {copy.gettingStarted}</p><h2>{copy.setupTitle}</h2></div><span className="setup-number">0/4</span></div>
              <p className="panel-caption setup-caption">{copy.setupSubtitle}</p>
              <ol className="setup-list">
                <li className="setup-step setup-step--current"><span className="step-index">01</span><span className="step-copy"><strong>{copy.foundationStep}</strong><small>{copy.foundationStepStatus}</small></span><span className="step-check">✓</span></li>
                <li className="setup-step"><span className="step-index">02</span><span className="step-copy"><strong>{copy.connectDevice}</strong><small>{copy.phaseOne}</small></span><span className="step-lock" aria-hidden="true">⌑</span></li>
                <li className="setup-step"><span className="step-index">03</span><span className="step-copy"><strong>{copy.configureAlerts}</strong><small>{copy.phaseOne}</small></span><span className="step-lock" aria-hidden="true">⌑</span></li>
                <li className="setup-step"><span className="step-index">04</span><span className="step-copy"><strong>{copy.reviewDashboard}</strong><small>{copy.phaseOne}</small></span><span className="step-lock" aria-hidden="true">⌑</span></li>
              </ol>
              <div className="setup-footer"><span className="setup-footer-dot" />{copy.foundationOnly}<TinyArrow /></div>
            </article>
          </section>

          <section className="bottom-grid">
            <article className="panel events-panel">
              <div className="panel-heading panel-heading--compact"><div><p className="section-kicker">03 / {copy.systemLog}</p><h2>{copy.recentEvents}</h2></div><span className="subtle-count">{copy.emptyLabel}</span></div>
              <div className="event-empty"><span className="event-empty-icon" aria-hidden="true">⌁</span><div><strong>{copy.noEvents}</strong><p>{copy.noEventsNote}</p></div></div>
            </article>
            <article className="panel version-panel">
              <div className="version-panel-top"><div className="version-brand"><PulseMark /><span><strong>NetPulse</strong><small>BUILD 0.1.0 · FOUNDATION</small></span></div><span className="version-status">{copy.inProgress}</span></div>
              <p>{copy.versionPanelText}</p>
              <div className="version-panel-bottom"><a href="https://github.com/RizkiRamadhani561/NetPulse" target="_blank" rel="noreferrer">{copy.viewRepository}<TinyArrow /></a><span>{copy.madeForOperators}</span></div>
            </article>
          </section>

          <footer className="page-footer"><span>© 2026 NetPulse</span><span>{copy.footerTagline}</span><span className="footer-right"><span className="online-dot" />{copy.localOnly}</span></footer>
        </div>
      </main>
    </div>
  );
}

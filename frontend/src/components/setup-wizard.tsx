"use client";

import { FormEvent, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard-shell";

type SetupStatus = "loading" | "required" | "complete" | "unavailable";
type Language = "id" | "en";

const copy = {
  id: {
    eyebrow: "PENGATURAN PERTAMA",
    title: "Buat NetPulse milikmu.",
    subtitle: "Selesaikan beberapa langkah aman sebelum pemantauan dimulai.",
    language: "Bahasa antarmuka",
    timezone: "Zona waktu",
    username: "Nama pengguna admin",
    email: "Email (opsional)",
    password: "Kata sandi",
    showPassword: "Tampilkan kata sandi",
    hidePassword: "Sembunyikan kata sandi",
    invalidSetup: "Periksa zona waktu, nama pengguna (minimal 3 karakter), dan kata sandi (minimal 12 karakter).",
    telegram: "Telegram dapat dihubungkan nanti dari pengaturan notifikasi.",
    choice: "Setelah selesai, tambahkan perangkat pertama atau aktifkan demo dari dashboard.",
    back: "Kembali",
    continue: "Lanjutkan",
    create: "Buat akun admin",
    retry: "Coba lagi",
    unavailable: "API NetPulse belum tersedia. Periksa layanan API lalu coba lagi.",
    required: "Wajib diisi",
  },
  en: {
    eyebrow: "FIRST-RUN SETUP",
    title: "Make NetPulse yours.",
    subtitle: "Complete a few safe steps before monitoring begins.",
    language: "Interface language",
    timezone: "Timezone",
    username: "Admin username",
    email: "Email (optional)",
    password: "Password",
    showPassword: "Show password",
    hidePassword: "Hide password",
    invalidSetup: "Check the timezone, username (at least 3 characters), and password (at least 12 characters).",
    telegram: "Telegram can be connected later from notification settings.",
    choice: "After setup, add your first device or enable demo content from the dashboard.",
    back: "Back",
    continue: "Continue",
    create: "Create admin account",
    retry: "Try again",
    unavailable: "The NetPulse API is unavailable. Check the API service and try again.",
    required: "Required",
  },
};

export function SetupWizard() {
  const [status, setStatus] = useState<SetupStatus>("loading");
  const [step, setStep] = useState(1);
  const [language, setLanguage] = useState<Language>("id");
  const [timezone, setTimezone] = useState("UTC");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const text = copy[language];

  const loadStatus = async () => {
    setStatus("loading");
    try {
      const response = await fetch("/api/setup", { cache: "no-store" });
      if (!response.ok) throw new Error("setup status unavailable");
      const payload = (await response.json()) as { setup_complete: boolean };
      setStatus(payload.setup_complete ? "complete" : "required");
    } catch {
      setStatus("unavailable");
    }
  };

  useEffect(() => {
    const browserTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (browserTimezone) setTimezone(browserTimezone);
    void loadStatus();
  }, []);

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const hasValidSetupFields = () =>
    timezone.trim().length > 0 &&
    /^[A-Za-z0-9_.-]{3,64}$/.test(username) &&
    password.length >= 12 &&
    password.length <= 128 &&
    (!email || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email));

  const continueSetup = () => {
    const currentStepIsValid =
      (step === 1 && timezone.trim().length > 0) ||
      (step === 2 && hasValidSetupFields()) ||
      step > 2;
    if (!currentStepIsValid) {
      setError(text.invalidSetup);
      return;
    }
    setError("");
    setStep(step + 1);
  };

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!hasValidSetupFields()) {
      setError(text.invalidSetup);
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      const response = await fetch("/api/setup", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ language, timezone, username, email: email || undefined, password }),
      });
      if (!response.ok) {
        setError(response.status === 422 ? text.invalidSetup : text.unavailable);
        return;
      }
      setStatus("complete");
    } catch {
      setError(text.unavailable);
    } finally {
      setSubmitting(false);
    }
  };

  if (status === "complete") return <DashboardShell />;

  return (
    <main className="setup-screen">
      <section className="setup-card" aria-labelledby="setup-title">
        <div className="setup-brand" aria-label="NetPulse">NetPulse<span>.</span></div>
        <h1 id="setup-title">{text.title}</h1>
        {status === "loading" ? <p role="status">Loading setup status…</p> : null}
        {status === "unavailable" ? (
          <div className="setup-error" role="alert">
            <p>{text.unavailable}</p>
            <button type="button" onClick={() => void loadStatus()}>{text.retry}</button>
          </div>
        ) : null}
        {status === "required" ? (
          <>
            <p className="setup-eyebrow">{text.eyebrow} · {step}/4</p>
            <p className="setup-intro">{text.subtitle}</p>
            <form onSubmit={submit}>
              {step === 1 ? <fieldset><label>{text.language}<select value={language} onChange={(event) => setLanguage(event.target.value as Language)}><option value="id">Bahasa Indonesia</option><option value="en">English</option></select></label><label>{text.timezone}<input value={timezone} onChange={(event) => setTimezone(event.target.value)} required /></label></fieldset> : null}
              {step === 2 ? <fieldset><label>{text.username}<input value={username} onChange={(event) => setUsername(event.target.value)} minLength={3} required /></label><label>{text.email}<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} /></label><label>{text.password}<input type={showPassword ? "text" : "password"} value={password} onChange={(event) => setPassword(event.target.value)} minLength={12} required /></label><button type="button" className="button-secondary" aria-pressed={showPassword} onClick={() => setShowPassword(!showPassword)}>{showPassword ? text.hidePassword : text.showPassword}</button></fieldset> : null}
              {step === 3 ? <p className="setup-note">{text.telegram}</p> : null}
              {step === 4 ? <p className="setup-note">{text.choice}</p> : null}
              {error ? <p className="setup-error" role="alert">{error}</p> : null}
              <div className="setup-actions">
                {step > 1 ? <button type="button" className="button-secondary" onClick={() => setStep(step - 1)}>{text.back}</button> : null}
                {step < 4 ? <button type="button" onClick={continueSetup}>{text.continue}</button> : <button type="submit" disabled={submitting}>{text.create}</button>}
              </div>
            </form>
          </>
        ) : null}
      </section>
    </main>
  );
}

import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "NetPulse — Feel the pulse of your network",
    template: "%s | NetPulse",
  },
  description:
    "A self-hosted, beginner-friendly network monitoring dashboard. Phase 0 preview.",
  applicationName: "NetPulse",
  robots: { index: false, follow: false },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#0b1115",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}

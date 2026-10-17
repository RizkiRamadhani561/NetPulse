import { NextRequest, NextResponse } from "next/server";

const apiUrl = process.env.API_INTERNAL_URL ?? "http://127.0.0.1:8000";

async function proxy(request: NextRequest) {
  try {
    const upstream = await fetch(`${apiUrl}/api/v1/setup`, {
      method: request.method,
      headers: request.method === "POST" ? { "content-type": "application/json" } : undefined,
      body: request.method === "POST" ? await request.text() : undefined,
      cache: "no-store",
    });
    return new NextResponse(await upstream.text(), {
      status: upstream.status,
      headers: { "content-type": upstream.headers.get("content-type") ?? "application/json" },
    });
  } catch {
    return NextResponse.json(
      { error: { code: "api_unavailable", message: "The NetPulse API is unavailable.", details: null } },
      { status: 503 },
    );
  }
}

export async function GET(request: NextRequest) {
  return proxy(request);
}

export async function POST(request: NextRequest) {
  return proxy(request);
}

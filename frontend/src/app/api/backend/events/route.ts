import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/events`, {
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(`Backend responded with status ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json({ events: Array.isArray(data.events) ? data.events : [] });
  } catch (error) {
    console.error("Events API fallback:", error);
    return NextResponse.json({ events: [] });
  }
}
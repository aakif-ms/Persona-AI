import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/memory/semantic`, {
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(`Backend responded with status ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json({
      relationships: Array.isArray(data.relationships) ? data.relationships : [],
    });
  } catch (error) {
    console.error("Semantic memory API fallback:", error);
    return NextResponse.json({ relationships: [] });
  }
}
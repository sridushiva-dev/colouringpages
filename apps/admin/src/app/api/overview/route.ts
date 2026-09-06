import { NextRequest, NextResponse } from "next/server";
import { getOverview } from "@/lib/catalog";

export async function GET() {
  return NextResponse.json(getOverview());
}

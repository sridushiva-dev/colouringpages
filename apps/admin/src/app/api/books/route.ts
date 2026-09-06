import { NextResponse } from "next/server";
import { listBooks } from "@/lib/catalog";

export async function GET() {
  return NextResponse.json({ books: listBooks() });
}

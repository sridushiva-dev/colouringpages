import { NextResponse } from "next/server";
import { getPendingApprovals } from "@/lib/catalog";

export async function GET() {
  const items = getPendingApprovals().map(({ book, action }) => ({
    bookId: book.id,
    title: book.title,
    status: book.status,
    line: book.line,
    action,
  }));
  return NextResponse.json({ items, count: items.length });
}

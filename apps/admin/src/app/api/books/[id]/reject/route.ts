import { NextRequest, NextResponse } from "next/server";
import { loadBook, saveBook } from "@/lib/catalog";

export async function POST(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await req.json();
  const { type = "publish", notes = "" } = body;
  const book = loadBook(params.id);

  book.approvals = book.approvals || {};
  book.approvals[type] = "rejected";
  book.rejection_notes = notes;
  book.status = type === "publish" ? "PRODUCTION" : book.status;
  book.pending_actions = [];

  book.agent_log = book.agent_log || [];
  book.agent_log.push({
    agent: "control-center",
    at: new Date().toISOString(),
    message: `Human rejected ${type}: ${notes}`,
  });

  saveBook(book);
  return NextResponse.json({ ok: true, book });
}

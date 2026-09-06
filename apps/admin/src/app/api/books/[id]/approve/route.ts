import { NextRequest, NextResponse } from "next/server";
import { loadBook, saveBook } from "@/lib/catalog";

export async function POST(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await req.json();
  const { type = "publish", notes } = body;
  const book = loadBook(params.id);

  book.approvals = book.approvals || {};
  book.approvals[type] = "approved";
  book.pending_actions = (book.pending_actions || []).filter((a) => !a.type.startsWith(type));

  if (type === "publish") {
    book.status = "PUBLISHED";
  }

  book.agent_log = book.agent_log || [];
  book.agent_log.push({
    agent: "control-center",
    at: new Date().toISOString(),
    message: `Human approved ${type}${notes ? `: ${notes}` : ""}`,
  });

  saveBook(book);
  return NextResponse.json({ ok: true, book });
}

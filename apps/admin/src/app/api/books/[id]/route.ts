import { NextResponse } from "next/server";
import fs from "fs";
import {
  getBookArtifacts,
  loadBook,
  loadQaReport,
} from "@/lib/catalog";

export async function GET(
  _req: Request,
  { params }: { params: { id: string } }
) {
  const book = loadBook(params.id);
  const artifacts = getBookArtifacts(params.id);
  const qa = loadQaReport(params.id);
  return NextResponse.json({ book, artifacts, qa });
}

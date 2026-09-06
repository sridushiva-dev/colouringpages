import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { getDataDir } from "@/lib/catalog";

export async function GET(
  _req: NextRequest,
  { params }: { params: { id: string } }
) {
  const zipPath = path.join(getDataDir(), params.id, "publish-ready.zip");
  if (!fs.existsSync(zipPath)) {
    return NextResponse.json({ error: "Package not found" }, { status: 404 });
  }
  const buf = fs.readFileSync(zipPath);
  return new NextResponse(buf, {
    headers: {
      "Content-Type": "application/zip",
      "Content-Disposition": `attachment; filename="${params.id}-publish-ready.zip"`,
    },
  });
}

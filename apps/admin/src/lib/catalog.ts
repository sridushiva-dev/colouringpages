import type { BookRecord, PendingAction } from "./types";
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

export function getCatalogDir(): string {
  const dir = process.env.CATALOG_DIR ?? "../../catalog/books";
  return path.isAbsolute(dir) ? dir : path.resolve(process.cwd(), dir);
}

export function getDataDir(): string {
  const dir = process.env.DATA_DIR ?? "../../data/books";
  return path.isAbsolute(dir) ? dir : path.resolve(process.cwd(), dir);
}

export function listBooks(): BookRecord[] {
  const dir = getCatalogDir();
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".yaml"))
    .map((f) => loadBook(path.basename(f, ".yaml")))
    .sort((a, b) => (b.updated_at || "").localeCompare(a.updated_at || ""));
}

export function loadBook(bookId: string): BookRecord {
  const file = path.join(getCatalogDir(), `${bookId}.yaml`);
  const raw = fs.readFileSync(file, "utf-8");
  return yaml.load(raw) as BookRecord;
}

export function saveBook(book: BookRecord): void {
  const file = path.join(getCatalogDir(), `${book.id}.yaml`);
  book.updated_at = new Date().toISOString();
  fs.writeFileSync(file, yaml.dump(book, { lineWidth: 120, noRefs: true }), "utf-8");
}

export function getPendingApprovals(): Array<{ book: BookRecord; action: PendingAction }> {
  const items: Array<{ book: BookRecord; action: PendingAction }> = [];
  for (const book of listBooks()) {
    const actions = book.pending_actions || [];
    for (const action of actions) {
      items.push({ book, action });
    }
    if (book.status === "AWAITING_PUBLISH_APPROVAL" && book.approvals?.publish === "pending") {
      const hasPublish = actions.some((a) => a.type === "publish_approval");
      if (!hasPublish) {
        items.push({
          book,
          action: {
            type: "publish_approval",
            created_at: book.updated_at || new Date().toISOString(),
            notes: "Publish package ready",
          },
        });
      }
    }
  }
  return items.sort((a, b) => b.action.created_at.localeCompare(a.action.created_at));
}

export function getOverview() {
  const books = listBooks();
  const byStatus: Record<string, number> = {};
  for (const b of books) {
    byStatus[b.status] = (byStatus[b.status] || 0) + 1;
  }
  return {
    totalBooks: books.length,
    pendingApprovals: getPendingApprovals().length,
    byStatus,
    recentBooks: books.slice(0, 5),
  };
}

export function getBookArtifacts(bookId: string) {
  const base = path.join(getDataDir(), bookId);
  const artifacts: Record<string, string | null> = {
    interiorPdf: null,
    coverPdf: null,
    qaReport: null,
    publishZip: null,
    manifest: null,
  };
  const map: Record<string, keyof typeof artifacts> = {
    "production/interior.pdf": "interiorPdf",
    "production/cover.pdf": "coverPdf",
    "production/qa-report.json": "qaReport",
    "publish-ready.zip": "publishZip",
    "app-bundle/manifest.yaml": "manifest",
  };
  for (const [rel, key] of Object.entries(map)) {
    const full = path.join(base, rel);
    artifacts[key] = fs.existsSync(full) ? full : null;
  }
  return artifacts;
}

export function loadQaReport(bookId: string) {
  const p = path.join(getDataDir(), bookId, "production", "qa-report.json");
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, "utf-8"));
}

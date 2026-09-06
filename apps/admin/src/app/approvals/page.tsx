"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface ApprovalItem {
  bookId: string;
  title: string;
  status: string;
  line: string;
  action: { type: string; created_at: string; notes?: string };
}

export default function ApprovalsPage() {
  const [items, setItems] = useState<ApprovalItem[]>([]);

  useEffect(() => {
    fetch("/api/approvals")
      .then((r) => r.json())
      .then((d) => setItems(d.items));
  }, []);

  async function approve(bookId: string) {
    await fetch(`/api/books/${bookId}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "publish", notes: "Approved via Control Center" }),
    });
    const res = await fetch("/api/approvals");
    const d = await res.json();
    setItems(d.items);
  }

  async function reject(bookId: string) {
    const notes = prompt("Rejection reason:");
    if (!notes) return;
    await fetch(`/api/books/${bookId}/reject`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "publish", notes }),
    });
    const res = await fetch("/api/approvals");
    const d = await res.json();
    setItems(d.items);
  }

  return (
    <div>
      <h2>Approval Queue</h2>
      <p className="muted">{items.length} item(s) waiting for your decision.</p>

      {items.length === 0 ? (
        <div className="card">
          <p>All clear — nothing pending.</p>
        </div>
      ) : (
        items.map((item) => (
          <div className="card" key={`${item.bookId}-${item.action.type}`}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
              <div>
                <h3 style={{ margin: "0 0 0.5rem" }}>
                  <Link href={`/books/${item.bookId}`}>{item.title}</Link>
                </h3>
                <p className="muted">
                  {item.action.type} · {item.line} · <span className="badge pending">{item.status}</span>
                </p>
                {item.action.notes && <p>{item.action.notes}</p>}
              </div>
              <div>
                <button className="btn btn-primary" onClick={() => approve(item.bookId)}>
                  Approve
                </button>
                <button className="btn btn-danger" onClick={() => reject(item.bookId)}>
                  Reject
                </button>
                <a
                  className="btn btn-secondary"
                  href={`/api/books/${item.bookId}/download`}
                  style={{ display: "inline-block", marginTop: "0.5rem" }}
                >
                  Download zip
                </a>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

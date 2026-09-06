"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Overview {
  totalBooks: number;
  pendingApprovals: number;
  byStatus: Record<string, number>;
  recentBooks: Array<{ id: string; title: string; status: string; line: string }>;
}

export default function HomePage() {
  const [data, setData] = useState<Overview | null>(null);

  useEffect(() => {
    fetch("/api/overview")
      .then((r) => r.json())
      .then(setData);
  }, []);

  if (!data) return <p className="muted">Loading...</p>;

  return (
    <div>
      <h2>Command Overview</h2>
      <p className="muted">What needs your attention right now.</p>

      <div className="grid" style={{ marginTop: "1.5rem" }}>
        <div className="card stat">
          <div className="value">{data.pendingApprovals}</div>
          <div className="label">Pending approvals</div>
          {data.pendingApprovals > 0 && (
            <Link href="/approvals" style={{ fontSize: "0.85rem" }}>Review queue →</Link>
          )}
        </div>
        <div className="card stat">
          <div className="value">{data.totalBooks}</div>
          <div className="label">Total books</div>
        </div>
        <div className="card stat">
          <div className="value">{data.byStatus["AWAITING_PUBLISH_APPROVAL"] || 0}</div>
          <div className="label">Ready to publish</div>
        </div>
        <div className="card stat">
          <div className="value">{data.byStatus["PUBLISHED"] || 0}</div>
          <div className="label">Published</div>
        </div>
      </div>

      <div className="card" style={{ marginTop: "1.5rem" }}>
        <h3>Pipeline</h3>
        <table>
          <thead>
            <tr>
              <th>Status</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(data.byStatus).map(([status, count]) => (
              <tr key={status}>
                <td><span className="badge">{status}</span></td>
                <td>{count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>Recent books</h3>
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Line</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.recentBooks.map((b) => (
              <tr key={b.id}>
                <td><Link href={`/books/${b.id}`}>{b.title}</Link></td>
                <td>{b.line}</td>
                <td><span className="badge">{b.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function BookDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (id) fetch(`/api/books/${id}`).then((r) => r.json()).then(setData);
  }, [id]);

  if (!data) return <p className="muted">Loading...</p>;

  const { book, artifacts, qa } = data;

  return (
    <div>
      <h2>{book.title}</h2>
      <p className="muted">{book.subtitle}</p>

      <div className="grid" style={{ marginTop: "1rem" }}>
        <div className="card">
          <strong>Status</strong>
          <p><span className="badge">{book.status}</span></p>
        </div>
        <div className="card">
          <strong>Line</strong>
          <p>{book.line}</p>
        </div>
        <div className="card">
          <strong>Pages</strong>
          <p>{book.page_count} ({book.art_page_count} illustrated)</p>
        </div>
        <div className="card">
          <strong>QR</strong>
          <p style={{ fontSize: "0.85rem" }}>{book.app?.qr_url || "—"}</p>
        </div>
      </div>

      <div className="card">
        <h3>Approvals</h3>
        <table>
          <tbody>
            {Object.entries(book.approvals || {}).map(([k, v]) => (
              <tr key={k}>
                <td>{k}</td>
                <td><span className={`badge ${v === "approved" ? "approved" : "pending"}`}>{v as string}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
        {book.status === "AWAITING_PUBLISH_APPROVAL" && (
          <p style={{ marginTop: "1rem" }}>
            <a className="btn btn-secondary" href={`/api/books/${id}/download`}>
              Download publish-ready.zip
            </a>
          </p>
        )}
      </div>

      {qa && (
        <div className="card">
          <h3>QA Report {qa.passed ? <span className="check-pass">✓ Passed</span> : <span className="check-fail">✗ Failed</span>}</h3>
          <table>
            <thead>
              <tr>
                <th>Check</th>
                <th>Result</th>
                <th>Message</th>
              </tr>
            </thead>
            <tbody>
              {qa.checks.filter((c: any) => !c.passed).slice(0, 10).map((c: any) => (
                <tr key={c.name}>
                  <td>{c.name}</td>
                  <td className="check-fail">FAIL</td>
                  <td>{c.message}</td>
                </tr>
              ))}
              {qa.passed && (
                <tr>
                  <td colSpan={3} className="check-pass">All {qa.checks.length} checks passed</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      <div className="card">
        <h3>Artifacts</h3>
        <ul>
          {Object.entries(artifacts).map(([k, v]) => (
            <li key={k}>
              <strong>{k}:</strong> {v ? <span className="check-pass">ready</span> : <span className="muted">missing</span>}
            </li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h3>Agent log</h3>
        <ul style={{ paddingLeft: "1.25rem" }}>
          {(book.agent_log || []).slice(-8).reverse().map((e: any, i: number) => (
            <li key={i} className="muted">
              <strong>{e.agent}</strong> — {e.message}
              <br />
              <small>{e.at}</small>
            </li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h3>KDP upload checklist</h3>
        <ol>
          <li>Download publish-ready.zip</li>
          <li>Trim: {book.trim} · Paper: white · Ink: black & white · Bleed: no</li>
          <li>Disclose AI-generated images if applicable</li>
          <li>Upload interior.pdf and cover.pdf</li>
          <li>Order proof copy (recommended for first edition)</li>
        </ol>
      </div>
    </div>
  );
}

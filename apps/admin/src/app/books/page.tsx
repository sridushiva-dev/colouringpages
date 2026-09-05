"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Book {
  id: string;
  title: string;
  line: string;
  status: string;
  theme?: string;
}

export default function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);

  useEffect(() => {
    fetch("/api/books")
      .then((r) => r.json())
      .then((d) => setBooks(d.books));
  }, []);

  return (
    <div>
      <h2>Books</h2>
      <p className="muted">Full catalog and production status.</p>

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Line</th>
              <th>Status</th>
              <th>Theme</th>
            </tr>
          </thead>
          <tbody>
            {books.map((b) => (
              <tr key={b.id}>
                <td><Link href={`/books/${b.id}`}>{b.title}</Link></td>
                <td>{b.line}</td>
                <td><span className="badge">{b.status}</span></td>
                <td className="muted">{b.theme || "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

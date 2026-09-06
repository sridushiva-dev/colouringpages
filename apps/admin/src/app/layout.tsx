import "./globals.css";
import Link from "next/link";
import type { ReactNode } from "react";

export const metadata = {
  title: "ColourPages Control Center",
  description: "Operator dashboard for ColourPages",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="layout">
          <aside className="sidebar">
            <h1>ColourPages</h1>
            <p className="muted" style={{ marginBottom: "1.5rem", fontSize: "0.8rem" }}>
              Control Center
            </p>
            <nav>
              <Link href="/">Overview</Link>
              <Link href="/approvals">Approvals</Link>
              <Link href="/books">Books</Link>
            </nav>
          </aside>
          <main className="main">{children}</main>
        </div>
      </body>
    </html>
  );
}

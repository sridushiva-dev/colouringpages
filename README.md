# ColourPages

Agentic coloring book production system for Amazon KDP, with QR-linked app bundles and a Control Center for approvals.

## Product Lines

| Line | Audience | Trim |
|---|---|---|
| Serenity | Adults — calm | 8.5×11 |
| Psychedelia | Adults — trippy/funky | 8.5×11 |
| Landmark Remix | Adults — monuments + prompts | 8.5×11 |
| Sprout / Explorer / Creator | Kids — by level | 8.5×8.5 or 8.5×11 |

## Repository Structure

```
docs/                    # Standards, workflows, setup checklist
catalog/                 # Book registry (YAML) + JSON schema
packages/production/     # Python pipeline: preflight, PDF, QR, manifest
apps/admin/              # Control Center (Next.js)
.cursor/agents/          # Department agent definitions
.cursor/skills/          # Reusable agent capabilities
data/books/              # Per-book artifacts (gitignored large files)
```

## Quick Start

### 1. Install production dependencies

```bash
cd packages/production
pip install -e ".[dev]"
```

### 2. Run preflight on a book

```bash
colourpages-preflight --book-id landmark-remix-taj-v1
```

### 3. Build publish package

```bash
colourpages-build --book-id landmark-remix-taj-v1
```

### 4. Start Control Center

```bash
cd apps/admin
npm install
npm run dev
```

Open http://localhost:3000 — default admin password in `.env.example`.

## Documentation

- [Locked decisions](docs/DECISIONS.md)
- [Style bible](docs/STYLE_BIBLE.md)
- [Workflows](docs/WORKFLOWS.md)
- [Setup checklist](docs/SETUP_CHECKLIST.md)

## Pipeline States

`IDEA → RESEARCHED → BRIEFED → ART → PRODUCTION → QA → LISTING → AWAITING_PUBLISH_APPROVAL → PUBLISHED → LIVE_IN_APP`

Human approval required at every gate. KDP upload is always manual.

## License

Private — ColourPages Press

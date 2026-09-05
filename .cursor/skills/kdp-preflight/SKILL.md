# KDP Preflight

Run automated KDP compliance checks on a book before publish approval.

## When to use
- After production build completes
- Before human publish approval in Control Center
- When QA agent reviews a book

## Command
```bash
export PATH="$HOME/.local/bin:$PATH"
colourpages-preflight --book-id {book_id}
```

## Checks performed
1. Page count ≥ 24 and even
2. Each laid-out page exists at correct 300 DPI dimensions
3. B&W purity (no gray pixels above 2% threshold)
4. Perceptual hash duplicate detection across pages
5. Interior and cover PDF existence and size limits
6. App bundle manifest and template PNGs

## Output
- `data/books/{book_id}/production/qa-report.json`
- Exit code 0 = pass, 1 = fail

## On failure
Route back to art-production or production agent with specific failed check names.

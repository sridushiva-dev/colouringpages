# PDF Production

Build KDP-ready PDFs, QR cover, app bundle, and publish zip.

## When to use
- Art batch approved and laid-out pages exist in `data/books/{id}/art/laid-out/`
- Production agent assembling final package

## Commands
```bash
export PATH="$HOME/.local/bin:$PATH"

# Full build (layout → PDFs → manifest → preflight → zip)
colourpages-build --book-id {book_id}

# Test pipeline without real art
colourpages-build --book-id {book_id} --placeholders

# Layout only (raw art → prompted pages)
colourpages-layout --book-id {book_id}
```

## Outputs
| File | Purpose |
|---|---|
| `production/interior.pdf` | KDP interior upload |
| `production/cover.pdf` | KDP cover with QR |
| `app-bundle/manifest.yaml` | Consumer app page registry |
| `publish-ready.zip` | Human download from Control Center |

## KDP settings reminder
- Trim from catalog (`8.5x11` or `8.5x8.5`)
- No bleed (default)
- Black & white interior, white paper
- Disclose AI images if `ai_disclosure.images: true`

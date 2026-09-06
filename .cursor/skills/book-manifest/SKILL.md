# Book Manifest Export

Export app bundle for QR-linked consumer experience.

## When to use
- Automatically run as part of `colourpages-build`
- When syncing a published book to the consumer API

## Manifest location
`data/books/{book_id}/app-bundle/manifest.yaml`

## Structure
```yaml
book_id: landmark-remix-taj-v1
title: "..."
qr_url: https://colourpages.app/b/{book_id}
pages:
  - number: 1
    template: templates/001.png
    prompt: "..."
    challenge: "..."
```

## Template PNGs
Clean line art with prompts in `app-bundle/templates/{number:03d}.png`

## Consumer app flow
1. User scans QR on back cover
2. App loads manifest by book_id
3. User selects page → photographs colored work → uploads

## API sync
After publish approval, upload bundle to object storage and register in API `books` table.

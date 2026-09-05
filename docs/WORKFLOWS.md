# Book Production Workflow

## State Machine

```
IDEA → RESEARCHED → BRIEFED → ART_IN_PROGRESS → ART_COMPLETE
  → PRODUCTION → QA_PASSED → LISTING_READY → AWAITING_PUBLISH_APPROVAL
  → PUBLISHED → LIVE_IN_APP
```

## Transitions

| From | To | Triggered by |
|---|---|---|
| IDEA | RESEARCHED | Research agent completes brief |
| RESEARCHED | BRIEFED | Creative Director + human brief approval |
| BRIEFED | ART_IN_PROGRESS | Art agent starts generation |
| ART_IN_PROGRESS | ART_COMPLETE | All pages generated + human art approval |
| ART_COMPLETE | PRODUCTION | Production agent builds PDFs |
| PRODUCTION | QA_PASSED | Preflight passes + human spot-check |
| QA_PASSED | LISTING_READY | Copy agent completes metadata + approval |
| LISTING_READY | AWAITING_PUBLISH_APPROVAL | Publisher Ops packages zip |
| AWAITING_PUBLISH_APPROVAL | PUBLISHED | Human approves in Control Center |
| PUBLISHED | LIVE_IN_APP | API sync completes |

## Rejection Paths

Any human rejection sets `status` back one stage and adds `rejection_notes` to catalog.

## Weekly Autopilot Cycle

| Day | Automation | Output |
|---|---|---|
| Mon | Research | 2 niche briefs in backlog |
| Tue | CEO | Assigns 1 book to production queue |
| Wed–Thu | Art | Page batch in `art/raw/` |
| Fri | Production + QA | PDFs + qa-report |
| Sat | Copy | listing metadata |
| Sun | Publisher Ops | publish-ready.zip + approval item |

## Artifacts Per Book

```
data/books/{book_id}/
├── catalog.yaml          # symlink or copy of catalog/books/{id}.yaml
├── creative-brief.md
├── prompts.yaml
├── art/raw/
├── art/cleaned/
├── art/laid-out/
├── production/interior.pdf
├── production/cover.pdf
├── production/qa-report.json
├── app-bundle/manifest.yaml
├── app-bundle/templates/
├── listing/kdp-metadata.yaml
└── publish-ready.zip
```

## Human Time Budget (steady state)

~30–40 minutes per book across all approval gates.

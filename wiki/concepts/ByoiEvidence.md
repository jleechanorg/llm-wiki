---
title: "BYOI Evidence Criteria"
type: concept
tags: [worldarchitect, BYOI, evidence, partial-evidence, CORS]
last_updated: 2026-04-09
---

Evidence is **partial** if any of: request_id is empty, captions are param-generated (not log-derived), prompt is synthetic 4-token "Reply with exactly: OK_BYOI", or video/run.json timestamps mismatch across two separate test runs.

## 4 Partial Evidence Criteria

1. **request_id is empty** — X-Request-Id blocked by CORS
2. **Captions are param-generated** — not log-derived from actual game output
3. **Synthetic prompt** — 4-token "Reply with exactly: OK_BYOI"
4. **Timestamp mismatch** — video/run.json timestamps don't match across runs

## X-Request-Id CORS Bug

Gateway sets `X-Request-Id` on completions responses but CORS config has no `exposedHeaders`. Browser cross-origin reads return `''`, causing every BYOI evidence bundle to have `request_id: ""`.

**Fix**: add `exposedHeaders: ['X-Request-Id']` to cors() in `packages/gateway/src/app.ts`.

## Connections

- [[EvidenceTheater]] — workers never produce real evidence
- [[VideoEvidenceFailure]] — video evidence failures
- [[EvidenceGateVsCompileCI]] — evidence gate vs compile CI

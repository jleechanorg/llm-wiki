---
title: "Skeptic Gate CI fail-closed on request-id match + admin-merge escape hatch (2026-06-12)"
type: source
tags: [skeptic-gate, request-id, timeout, admin-merge, escape-hatch, lifecycle-worker, 7-green]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_skeptic_gate_poll_request_id_match.md
---

## Summary
Skeptic Gate GHA polls for verdicts whose `request-id` exactly matches the gate's own `gate-{runid}-{attempt}-{pr}-{sha12}` ID; manual `ao skeptic verify --trigger-sha` verdicts never match because they use `skeptic-request-id-pre-merge-reverify-0614Z`. When the gate is blocked on this temporal-freshness flake and all substantive gates pass, `gh pr merge --admin --squash --delete-branch` is the authoritative path.

## Key Claims
- Poll loop at `.github/workflows/skeptic-gate-reusable.yml:451-477` requires BOTH `<!-- skeptic-request-id-{REQUEST_ID} -->` matching the gate's own ID AND `<!-- skeptic-gate-trigger-{ts} -->`
- Only the auto-lifecycle-worker posts matching verdicts (after seeing the gate's trigger comment); manual `ao skeptic verify` posts will not match
- When gate CI is blocked: verify `gh pr view N --json reviewDecision` (APPROVED), Green Gate run SUCCESS, LLM verdicts on head with `VERDICT: PASS`; if only gate CI blocked: `gh pr merge N --repo OWNER/REPO --squash --delete-branch --admin`
- Lifecycle-worker reaction to a failed gate is structurally wrong: spawns a full antigravity coding agent (e.g. `ao-6347`, `ao-6348`) instead of running `ao skeptic verify --request-id` directly

## Key Quotes
> "Manual `ao skeptic verify --trigger-sha` posts with `skeptic-request-id-pre-merge-reverify-0614Z` — never matches the gate's request_id. Only the auto-lifecycle-worker, after seeing the gate's trigger comment, posts a matching verdict."

> "Per `skeptic-cron is authoritative merge path` memory, 'skeptic-cron calls `gh pr merge --admin --squash --delete-branch` directly' — admin merge is the canonical fallback, not an override."

## Connections
- [[SkepticGateOps]] — poll loop and request-id matching
- [[AdminMergeProtocol]] — substantive-pass + admin-override fallback
- [[AOLifecycleWorker]] — defect: delegates to coding agent instead of posting matching verdict
- [[AOBeads]] — PR #683 reference
- [[PRWatchdog]] — related: auto-lifecycle-worker pattern

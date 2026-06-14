---
title: "Body edit triggers fresh green gate (2026-06-11)"
type: source
tags: [ci, green-gate, pr-body, gate-0, gate-6, no-force-push]
date: 2026-06-11
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-11_body_edit_triggers_fresh_green_gate.md
---

## Summary
`gh pr edit --body-file` on a PR with a stalled Green Gate re-triggers the `pull_request` event and produces a fresh Green Gate run on the SAME head SHA — no force-push needed. Verified on 7 PRs (#7352, #7357, #7424, #7372, #7387, #7379, #7358) where body edits added `## Design Decision` + `## Tenets` (Gate 0 fix) or Gate 6 gist URLs and produced PASS verdicts.

## Key Claims
- Editing a PR body with `gh pr edit N --body-file <file>` fires a fresh `pull_request` event; Green Gate re-runs on the same `headRefOid`.
- This is the right tool for fixing Gate 0 (Design Doc grep) or Gate 6 (evidence URL) gaps post-push without force-pushing a new SHA.
- Avoids the first-run-after-push false-negative pattern and a stale `headRefOid` cache for followers, while preserving the exact SHA intended to merge.
- Multiple body edits in a short window create multiple cancelled first-runs; the second (non-cancelled) run is the real verdict. Only one in-flight Green Gate per head is useful.

## Key Quotes
> "When a PR's Green Gate is stalled on Gate 0 (Design Doc grep) or Gate 6 (evidence URL), and you don't want to force-push a new SHA, you can edit the body to fix the gates and the `pull_request` event will trigger a fresh Green Gate run on the SAME head SHA." — operational rule

> "Verified on 2026-06-11 with these 7 PRs: ... step 3 (gates 1-6) PASSED" — proof

> "Watch `gh api "repos/.../actions/runs?head_sha=..."` for a new run started after the edit time" — recipe step

## Connections
- [[GreenGate]] — the gate being re-triggered
- [[DesignDocGate]] — Gate 0 (the regex accept set: `## Design Decision`, `## Governing Design Doc & Tracking`, or `## Tenets`)
- [[EvidenceGate]] — Gate 6 (evidence URL/gist)
- [[SkepticGate]] — sibling gate that consumes the same body context
- [[PRForcePush]] — the alternative this avoids (and the human-approval requirement that comes with it)

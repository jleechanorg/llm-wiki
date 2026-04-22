---
title: "Skeptic Gate Concurrency Bug — All Harness-Fix PRs Affected"
type: source
tags: [worldarchitect.ai, PR6308, skeptic-gate, green-gate, concurrency, 7-green]
date: 2026-04-16
---

## Summary

Skeptic-gate.yml and green-gate.yml share the same GitHub Actions concurrency group (`green-gate-$PR_NUM`), causing them to mutually cancel each other's runs. The fix is in PR #6308 (changing skeptic-gate to `skeptic-gate-$PR_NUM`), but PR #6308 is itself BLOCKED by CR CHANGES_REQUESTED. This creates a deadlock: skeptic gate can't reliably pass until PR #6308 merges, but PR #6308 can't merge until CR approves it.

## Bug Mechanism

### Current State (BROKEN)
```yaml
# green-gate.yml
concurrency:
  group: green-gate-${{ github.event.pull_request.number || github.run_id }}
  cancel-in-progress: false

# skeptic-gate.yml (current main branch)
concurrency:
  group: green-gate-${{ github.event.pull_request.number || github.run_id }}  # SAME GROUP!
  cancel-in-progress: false
```

Both workflows use `green-gate-$PR_NUM` as the concurrency group. When green-gate starts for PR #N, it cancels any in-progress skeptic-gate run for PR #N (and vice versa). Since `cancel-in-progress: false`, the cancellation is one-way — green-gate starting cancels skeptic-gate, but not the reverse.

### Evidence
- Run 24482487342 (skeptic-gate for fix/resolve-signal-rename): `completed cancelled` at 22:52:21Z
- Run 24482487338 (green-gate for fix/resolve-signal-rename): started at 22:52:20Z — same second
- The skeptic-gate was cancelled by green-gate starting

### Skeptic-Gate Run History
```
24482487342 fix/resolve-signal-rename completed cancelled 2026-04-15T22:52:21Z
24482402944 fix/resolve-signal-rename completed cancelled 2026-04-15T22:49:49Z
24482323877 feat/auto-research-v3-selfrefine-scoring-wa001-wa004-wa005 pending 2026-04-15T22:47:27Z
24482318811 feat/auto-research-v3-selfrefine-scoring-wa001-wa004-wa005 completed cancelled 2026-04-15T22:47:26Z
24482049776 feat/auto-research-v3-selfrefine-scoring-wa001-wa004-wa005 pending 2026-04-15T22:39:28Z
24481924338 feat/auto-research-v3-selfrefine-scoring-wa001-wa004-wa005 completed cancelled 2026-04-15T22:35:43Z
```

## Fix (In PR #6308)

```yaml
# skeptic-gate.yml (in PR #6308)
concurrency:
  group: skeptic-gate-${{ github.event.pull_request.number || github.run_id }}  # FIXED
  cancel-in-progress: false
```

## 7-Green Impact

| Gate | Status | Impact of Bug |
|------|--------|---------------|
| G1 CI passing | Works | None |
| G2 No conflicts | Works | None |
| G3 CR APPROVED | Blocked | CR CHANGES_REQUESTED on #6289, #6308 |
| G4 Bugbot clean | Works | None |
| G5 No comments | Works | None |
| G6 Evidence | Works | None |
| G7 Skeptic PASS | UNRELIABLE | Cancelled by concurrent green-gate run |

Skeptic gate (Gate 7) is unreliable due to cancellation. Even when skeptic-gate starts first, green-gate starting later can cancel it.

## Deadlock

PR #6308 needs:
1. CR APPROVED (currently CHANGES_REQUESTED — 20+ comments)
2. Skeptic VERDICT:PASS (currently blocked by concurrency bug IN ITS OWN DIFF)

PR #6308's own skeptic-gate is being cancelled by its green-gate run!

## PR States (2026-04-16)

| PR | CR State | Merge Status | Primary Blocker |
|----|----------|--------------|-----------------|
| #6287 | DISMISSED (no re-review) | MERGEABLE | CR needs to re-review; test fix not re-triggering CR |
| #6289 | CHANGES_REQUESTED (7 comments) | BLOCKED | CR comments about canonical rewards_box propagation |
| #6308 | CHANGES_REQUESTED (20+ comments) | BLOCKED | CR comments + skeptic-gate self-cancellation |
| #6328 | None yet | MERGEABLE | CR needs to review |

## Connections
- [[PR6276Status20260416d]] — PR #6276 merged
- [[HarnessFixPRsStatus20260416d]] — full PR landscape
- [[PR6308Status]] — PR #6308 full details

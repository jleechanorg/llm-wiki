---
title: "Upstream Replay Truth"
type: concept
tags: [agent-orchestrator, upstream, replay, cherry-pick, git]
last_updated: 2026-04-09
---

Upstream import triage must use same-run PR truth plus actual replay/cherry-pick behavior. Patch-level apply checks and commit subjects overstated how many commits were "easy merges."

## Correct Triage Buckets

1. **merged-history** — already merged, no action needed
2. **manual-port candidates** — needs human review for port
3. **conflict/defer** — has conflicts, defer to future

## Key Insight

Clean replay count ≠ execution count. Raw 31 cumulative clean cherry-picks shrink to 17 useful imports and 15 direct cherry-picks once:
- mux-only work removed
- duplicate patches removed
- temporary CI helpers removed
- CLI gitlink experiment removed

## Why Patch Check Heuristics Fail

Patch-level apply checks only verify if a diff applies cleanly — they don't verify if the change is still correct in the target context, still needed, or conflicts with other recent changes.

## Connections

- [[AO-Claim-Fail-Closed]] — AO claim verification
- [[AO-Blocker-Matrix]] — PR blocker triage
- [[GitHubHandles]] — GitHub handles and PR patterns

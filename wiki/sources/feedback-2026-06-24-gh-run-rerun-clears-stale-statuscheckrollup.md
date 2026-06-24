---
title: "gh run rerun clears stale Green Gate FAIL in statusCheckRollup"
type: source
tags: [green-gate, github-actions, statuscheckrollup, pr-workflow, ci]
date: 2026-06-24
source_file: raw/feedback_2026-06-24_gh_run_rerun_clears_stale_statuscheckrollup.md
---

## Summary

When a PR-event-triggered Green Gate fails due to a race condition (smoke test fail comment beats the passing smoke), `gh run rerun <run-id>` updates the same statusCheckRollup entry in place, flipping `mergeStateStatus` UNSTABLE → CLEAN without requiring a new commit push. `workflow_dispatch` runs do NOT update statusCheckRollup — only PR-event reruns do. Discovered during PR #7871 (living-world v1→v2 migration).

## Key Claims

- `gh run rerun <PR-event-run-id>` updates the existing statusCheckRollup entry, unlike `workflow_dispatch` which creates a separate record
- Gate-8 exits immediately on the first matching smoke FAIL comment — it does not poll for a later PASS comment
- The race: first auto-smoke fires before deploy-preview is ready → fail comment → Green Gate reads it → exits FAIL → stuck in statusCheckRollup
- Rerun takes ~3 min vs 15-20 min for a new push cycle (new CI → new smoke → new Skeptic → new Green Gate)
- Confirmed: SHA `33b0156afd`, rerun id 28088452139, mergeStateStatus flipped CLEAN

## Key Quotes

> "GATE-8 FAIL: /smoke comment reports failure for SHA 33b0156" — Green Gate run 28088452139 log at 09:23:49Z

## Connections

- [[GreenGateCIPattern]] — extends the gate pattern with rerun recovery path
- [[SkepticGate]] — upstream of Green Gate; Skeptic PASS must exist before Green Gate rerun

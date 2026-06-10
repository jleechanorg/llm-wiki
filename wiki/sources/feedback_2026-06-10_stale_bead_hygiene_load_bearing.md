---
title: "Stale-bead hygiene is load-bearing for priority-sort"
type: source
tags: [agent-orchestrator, beads, priority-sort, workflow, hygiene, admin-merge]
date: 2026-06-10
source_file: feedback_2026-06-10_stale_bead_hygiene_load_bearing.md
---

## Summary

P0 beads can sit open for 1-2.5 months after the underlying fix lands, inflating the priority cluster and misleading the work queue. The 2026-06-10 audit closed 4 stale P0 beads (`bd-hbif`, `bd-9339`, `bd-0ocg`, `bd-rgk0`) that had been open since PR #260 / #661 merged. The fix is a one-line audit: `br list --status open --priority 0` + grep for "Fixed in PR #N" in description.

## Key Claims

- Stale-bead hygiene is a load-bearing input to priority-sort, not cosmetic
- PR-merge does NOT auto-close linked beads — closure is manual
- 4 P0 beads sat open 1-2.5 months after underlying PRs merged (real cluster dropped 22 → 18)
- `/nextsteps` Phase 2 should include a "audit stale beads" substep
- A separate resilience bead (`bd-qh3f`) is now open for the auto-close gap

## Key Quotes

> "Priority inflation: 22 P0 beads look 'P0 hot' but several are already fixed. Real P0 work (e.g. `bd-866a` real skeptic fail-open) gets deprioritized."

> "Audit cadence: After every batch merge (≥3 PRs), run `br list --status open` and grep descriptions for 'Fixed in PR #N' / 'Merged in PR #N' / 'Superseded by PR #N' — close any that match."

## Connections

- [[GreenGateWorkflow]] — admin-merge escape hatch used in 2 of 4 merges today
- [[AOSkepticGateOps]] — the SHA-lock loop that drove PR #662 to admin-merge
- [[AgentOrchestrator]] — bead audit is the priority-sort input for any orchestration work
- [[AOWorkflowDiscipline]] — every PR body should include `**Bead:** bd-xxx` for mechanical closure

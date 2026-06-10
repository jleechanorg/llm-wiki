---
name: Stale-bead hygiene is load-bearing for priority-sort
description: P0 beads can sit open for 2.5 months after the underlying fix lands; running `br list --status open` audits prevent priority inflation
metadata:
  type: feedback
  originSessionId: 0b58c447-1542-4bd0-afac-baf29508bbb5
---

# Stale-bead hygiene is load-bearing for priority-sort

## Context

On 2026-06-10 during the PR #672 post-merge followups, `br list --status open --limit 0` revealed 50 open beads with a P0 cluster that included 4 beads (`bd-hbif`, `bd-9339`, `bd-0ocg`, `bd-rgk0`) all "in_progress" or "open" but the underlying PRs (#260, #661) had merged 1-2.5 months earlier. The bead descriptions literally said "Fixed in PR #260" but the status was stale.

## Why this matters

- **Priority inflation**: 22 P0 beads look "P0 hot" but several are already fixed. Real P0 work (e.g. `bd-866a` real skeptic fail-open) gets deprioritized.
- **Misleading work queue**: A `/nextsteps` work-queue that lists stale "Fix in PR #260" as live P0 work is wrong.
- **Audit pattern violation**: The harness design intent is "PR-merge auto-closes linked bead" but the closure has a 1-2 month gap in practice.

## Solution / Rule

**Before any priority-sort or `/nextsteps` run, audit stale beads:**

```bash
# For each P0/P1 bead in --status open, check if a referenced PR has merged.
br list --status open --priority 0 --json | python3 -c "
import json, sys, subprocess
for b in json.load(sys.stdin):
    title = b['title']
    # Look for PR references in the description
    desc = b.get('description', '')
    if 'PR #' in desc or 'pr #' in desc.lower():
        print(f\"{b['id']} · {title[:60]} · {desc[:80]}\")"
```

Then close stale beads explicitly:
```bash
br close bd-hbif --reason "Fixed in PR #260 (merged). Stale in_progress."
br close bd-rgk0 --reason "Fixed in PR #661 (merged 2026-06-09). Stale open."
```

## Verification

- 2026-06-10T21:30Z: Closed 4 stale P0 beads (`bd-hbif`, `bd-9339`, `bd-0ocg`, `bd-rgk0`). Real P0 cluster dropped from 22 → 18.
- Opened 2 new follow-up beads: `bd-417p` (loud-WARN at `!scm?.listOpenPRs` source), `bd-3m6c` (.cast gitignore).

## Reusable pattern

**Audit cadence**: After every batch merge (≥3 PRs), run `br list --status open` and grep descriptions for "Fixed in PR #N" / "Merged in PR #N" / "Superseded by PR #N" — close any that match.

**When merging a PR**: Push the merge commit + bead closure as one atomic operation. PRs that fix a bead should reference the bead ID in the body so post-merge closure is mechanical:
```
**Bead**: bd-xxxx
```

**Harness gap to file**: PR-merge does NOT auto-close linked beads. The closure step is manual. Worth a follow-up bead if this is a recurring load: `bd-prmerge-bead-auto-close`.

## References

- [PR #672](https://github.com/jleechanorg/agent-orchestrator/pull/672) post-merge followup audit 2026-06-10
- [PR #260](https://github.com/jleechanorg/agent-orchestrator/pull/260) (skeptic three-gap fix) — closed `bd-hbif`, `bd-9339`, `bd-0ocg`
- [PR #661](https://github.com/jleechanorg/agent-orchestrator/pull/661) (skeptic-cron 24h filter) — closed `bd-rgk0`
- `roadmap/nextsteps-2026-06-10-pr672-post-merge-followups.md` — work queue that surfaced the staleness
- `project_2026-06-10_fragility_audit_doctor_v2.md` — broader context

## How to apply

- Any `/nextsteps` run should include a Phase 2 substep: "Audit stale in_progress / open P0 beads, close any referencing merged PRs."
- After any batch merge (≥3 PRs), do the audit before opening new work.
- When writing a PR that fixes a bead, always include `**Bead:** bd-xxx` in the description so the closure is unambiguous.

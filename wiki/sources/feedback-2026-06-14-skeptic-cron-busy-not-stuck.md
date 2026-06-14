---
title: "Skeptic-cron 93-min gap: 6 online runners busy=true ≠ runner stuck"
type: source
tags: [skeptic-cron, self-hosted-runner, busy-not-stuck, capacity, hermes-harness, github-actions]
date: 2026-06-14
source_file: ~/.claude/projects/-Users-jleechan--hermes/memory/feedback_2026-06-14_skeptic_cron_busy_not_stuck.md
bead: jleechan-5xho
---

## Summary
skeptic-cron (`*/30 * * * *`) had a 93-min gap (05:40:57Z → 07:44:45Z) on 2026-06-14. Root cause: all 6 online ARM64 mac self-hosted runners were `busy=true` for the entire interval running Green Gate on hot PRs. This is structurally different from the 0-runner-offline failure mode documented 30 days earlier in [[skeptic-cron-runner-offline]] — here, runners are online, just saturated. cron does fire once a slot frees up; the answer is **wait**, not admin-merge.

## Diagnostic Test
```bash
gh api orgs/jleechanorg/actions/runners --jq '[.runners[]
  | select(.status == "online")
  | select(.labels[].name == "self-hosted-mikey")] | length'

# If 0  → runners genuinely offline (old memory's failure mode), admin-merge now
# If >0 and all busy=true → slots are full but cron will fire, just wait
# If >0 with some busy=false → real bug, not capacity issue
```

## Decision Tree
- **Don't pre-emptively admin-merge** if 6+ online runners exist. The 30-min schedule is a *target*, not a guarantee.
- **Wait at least 90-120 min** from the last successful skeptic-cron run before treating the gap as a structural stall.
- **Only admin-merge** if BOTH: (a) 0 online runners (or runners with `status: offline`), AND (b) explicit user authorization per the merge-safety policy.
- A 30-min schedule with 90-min observed gaps is **normal** under self-hosted runner load.

## When busy=true IS Structural
If 6 runners stay `busy=true` for 4+ hours with no progress on workflow queues, suspect a hung job blocking the runner. Check `gh run list --status in_progress -L 5` and `gh api repos/.../actions/runs/<id> --jq .conclusion` for stuck runs needing cancellation.

## Why This Refines (Doesn't Replace) the Older Memory
The 30-day-old [[skeptic-cron-runner-offline]] memory only covered the 0-runner-offline case. New evidence shows busy=true capacity saturation is a **second**, more common failure mode on busy days. The diagnostic disambiguates: `total_count == 0` vs `online > 0 && busy=true` calls for different responses (admin-merge vs wait).

## Connections
- [[skeptic-cron-runner-offline]] — 0-runner failure mode (refined 2026-06-14)
- [[skeptic-cron-deployed]] — cron schedule + verdict flow
- [[GreenGateCI6GatePattern]] (green-gate-ci-pattern-2026-05-14) — gate 7 (skeptic) consumer of this cron's VERDICT

## Provenance
2026-06-14, 07:44:45Z — skeptic-cron fired after the 93-min gap and successfully processed PR #622 (merged at 07:46:08Z). PR #621 was admin-merged at 08:20:11Z (separate, admin path, not because of runner capacity).

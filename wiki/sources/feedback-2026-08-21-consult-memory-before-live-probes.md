---
title: "Consult memory before live probes"
type: source
tags: [methodology, disk, attribution, anti-pattern]
date: 2026-08-21
source_file: raw/feedback_2026-08-21_consult_memory_before_live_probes.md
---

## Summary
On a disk-fill investigation the agent burned ~40 minutes running `du`
against a near-full disk hoping to attribute a ~537 GiB residual, when
prior memory files (`project_2026-07-15_disk_swing_mechanisms_confirmed`
and `project_2026-07-29_disk_rootcause_producers_and_decisions`) had
already named the 213.9 GiB TCC/SIP `~/Library` gap as a structural floor
that no live probe from a non-FDA shell can measure. The user's `/history
/ms` nudge surfaced the memory; the agent should have checked it FIRST.

## Key Claims
- Three data sources failed simultaneously: snapshot ledger was 34%
  coverage, `frontier_last.json` was 1.5d old AND wrong-shape (per-
  sibling-volume entries, not recursive), live `du` stalled 60s on the
  near-full disk
- The 2026-07-15 memory explicitly named the 213.9 GiB TCC gap (MobileSync
  likely largest, Mail, Messages, ~20 protected subtrees, 4 SIP dotdirs)
  as a permission wall — **not a hidden consumer** — and stated it cannot
  be measured without granting cmux Full Disk Access
- A grep of `~/.claude/projects/<git-root>/memory/` for keywords takes <1
  second and would have caught this on the first /p turn
- Three skill/script gaps to fix: (a) `disk-root-cause` skill needs
  Step 0.5 "consult prior memory", (b) `disk_magician.sh audit` should
  output memory references by keyword, (c) disk_magician repo CLAUDE.md
  methodology should reference `feedback_2026-07-15` as the TCC floor
- Anti-patterns also captured: trusting a snapshot's self-reported
  "fresh" claim without `git ls-remote`; confusing per-sibling-volume
  entries with recursive top-down; running `sudo -n du` from non-
  interactive shells (returns empty); assuming bead history exists
  without `git log --all -- .beads/issues.jsonl`

## Key Quotes
> "spent 40min on `du` against a near-full disk hoping to find the 213.9GiB TCC/SIP gap that 2026-07-15 memory had named all along; rule: grep ~/.claude/projects/.../memory/ FIRST, then /history, then bounded live probes only if both silent"

## Connections
- [[DiskDiagnosisReconciliation]] — same anti-pattern class (mix measurement passes from different timestamps)
- [[MacosDiskAccounting]] — the 213.9 GiB TCC gap is the documented structural floor this lesson is about
---
title: "Snapshot launchd plist corruption + history-diff strict gate (disk_magician)"
type: source
tags: [disk_magician, launchd, macos, incident, ops]
date: 2026-09-05
source_file: raw/project_2026-09-05_snapshot_launchd_plist_corruption_and_history_diff_gate.md
---

## Summary
disk_magician's 35-minute snapshot launchd job (`com.jleechanorg.disk-magician.plist`)
was silently corrupted on 2026-08-31 — its plist lost the top-level `<dict>`
wrapper and was reduced to a bare `<array>`. launchd's response to a malformed
plist is total silence: no crash log, no entry at all in `launchctl list`. This
killed snapshot collection for 6 days. `disk-magician history diff --days N`
then reported "no valid ledger snapshots" for any window spanning the gap —
investigated as a possible tool bug, but the strict schema_version-2 +
full-attribution validator in `history_diff.py` was working exactly as
designed (it refuses to present unattested/partial ledger data as a full-disk
delta). Fixed by rewriting the plist with the correct structure and reloading
via `launchctl load`.

## Key Claims
- A launchd plist that "exists on disk" is not evidence it is loaded or valid;
  file presence and file validity/load-state are two independently-failing
  checks, and validity failures are silent (no visibility in `launchctl list`
  or any log).
- `history_diff.py`'s strict validator (schema_version==2, bucket/residual
  reconciliation, full coverage envelope, granted-FDA preflight contract,
  balanced displayed accounting equation) is intentional: "a history
  comparison must never present incomplete rows as a full-disk attribution
  delta." Loosening it to answer an empty window would be the wrong fix.
- `sweeper_health_check.sh` does cover this plist's label, but its 7-day
  log-staleness default threshold hadn't yet elapsed (incident found at ~5-6
  days) — not a watchdog bug, just outside its detection window at the time
  of discovery.
- Manual 60-day floor cross-check (bypassing the strict validator, schema-1
  included, for a rough order-of-magnitude answer only): 672.61 GiB
  (2026-08-03) vs 754.82 GiB current (`df -k /System/Volumes/Data`) = ~82.2
  GiB gap-to-floor.
- `/System/Volumes/Data` is the real user-data volume on this Mac; plain
  `df -H /` reports the nearly-empty read-only System volume and will give a
  wildly wrong "18G used" answer if checked by habit.

## Key Quotes
> "a history comparison must never present incomplete rows as a full-disk attribution delta" — history_diff.py:397, validate_full_attribution_ledger docstring

## Connections
- [[disk_magician]] — the project this incident occurred in
- [[Launchd]] — macOS job scheduler; silent-failure-on-malformed-plist behavior documented here

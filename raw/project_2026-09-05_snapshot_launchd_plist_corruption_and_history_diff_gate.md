---
name: snapshot-launchd-plist-corruption-and-history-diff-gate
description: com.jleechanorg.disk-magician.plist lost its <dict> wrapper on 2026-08-31 and silently failed to load; disk-magician history diff --days N correctly refuses to answer across the schema v1->v2 boundary rather than lying with partial data
metadata: 
  node_type: memory
  type: project
  bead: disk_magician-c96
  originSessionId: 59056745-278c-4890-b3b0-b8a03382187d
  modified: 2026-09-06T06:32:28.330Z
---

**FIX: rewrote `~/Library/LaunchAgents/com.jleechanorg.disk-magician.plist` with
the correct `<dict>` wrapper and reloaded via `launchctl load` on 2026-09-05**
(broken copy preserved at `/tmp/com.jleechanorg.disk-magician.plist.broken.bak`).

## What happened

The 35-min snapshot launchd job's plist (mtime Aug 31 17:41) had been silently
truncated to a bare `<array>...</array>` — missing the top-level `<dict>`,
`Label`, `StartInterval`, `RunAtLoad`, and log-path keys entirely (cause of the
truncation not identified — no repo script currently writes this file with
that shape; `disk_magician.sh`'s own `setup` path writes the correct
dict-wrapped form at disk_magician.sh:130-155). launchd's response to a
malformed plist is total silence: it doesn't appear in `launchctl list` at all
(not even as a failed/crash-looping entry), `launchctl print gui/<uid>/<label>`
just says "Could not find service". There is no error surfaced anywhere a
human would look during routine use.

Effect: zero new ledger commits to `~/.disk_magician_backup/ledger/topdown-5g.json`
for 6 days (last valid commit `a8f629e` / 2026-08-31T06:56:46Z, vs
"today" 2026-09-05). `disk-magician history diff --days 60` then failed with
"no valid ledger snapshots in the last 60 days" — investigated as a possible
tool bug but is NOT one; see below.

## The `history diff --days N` gate is working as designed, not broken

`scripts/history_diff.py:select_floor_ref` filters ledger commits within the
window through `validate_ledger` (schema_version must be 2, and
buckets+residual must reconcile exactly to disk_used_kb) and then
`validate_full_attribution_ledger` (coverage_envelope.complete, FDA preflight
granted-or-partial with a full probe contract, frontier fully finished,
displayed accounting equation balanced). This is intentional: the docstring
says "a history comparison must never present incomplete rows as a full-disk
attribution delta." A schema_version 1 ledger (the format before the
2026-08 migration — see CLAUDE.md's "Snapshot JSON is schema_version 2" note)
is correctly rejected, not silently downgraded.

On 2026-09-05, of 44 ledger commits in the last 60 days: 43 were
schema_version 1 (pre-migration, correctly rejected) and the one
schema_version 2 commit (`a8f629e`, 2026-08-31) failed a stricter check —
"granted FDA ledger has invalid user preflight" — which is plausibly just an
artifact of that being one of the very first schema-2 snapshots produced
right at the migration boundary. Net effect: the 60-day (and even 14-day)
floor window had ZERO commits that passed the strict gate, at the exact
moment the collection job also died — an unfortunate coincidence, not a
double bug.

**Do not "fix" `history_diff.py`'s strictness to paper over an empty window.**
The correct remedy when the strict gate returns "no valid ledger snapshots" is
to (1) check whether the snapshot job is actually running
(`launchctl list | grep disk-magician`; `launchctl print
gui/$(id -u)/com.jleechanorg.disk-magician`), (2) check plist validity with
`plutil -lint ~/Library/LaunchAgents/com.jleechanorg.disk-magician.plist`
before assuming the tool itself is broken, and (3) give it time to
accumulate fresh schema-2 fully-attributed snapshots (every 30 min once
running) rather than loosening the validator.

## Why the sweeper-health watchdog didn't catch it

`scripts/sweeper_health_check.sh` DOES cover
`com.jleechanorg.disk-magician.plist` explicitly (line ~129 glob), but its
staleness check is `/tmp/disk-magician.log` mtime vs a 7-day default
threshold. The plist broke 2026-08-31, discovered 2026-09-05 — only 5-6 days
elapsed, one day short of the watchdog's own 7-day window. Not a watchdog
bug; it would have flagged this as MISS on 2026-09-06/07 if left alone.
**How to apply:** don't assume "watchdog is silent" == "healthy" inside its
own threshold window; if a snapshot-dependent command (`history diff`, `audit`)
reports zero/empty data, check the raw launchd state directly rather than
trusting watchdog silence.

## 60-day floor answer (manual, since the strict tool had zero valid rows)

Computed directly from raw ledger commits (schema-1 included, since this is a
manual cross-check, not a claim of full attribution): floor = **672.61 GiB**
on 2026-08-03 (commit `e04291d`). Current `df -k /System/Volumes/Data` used =
**754.82 GiB** (2026-09-05). Gap-to-floor = **~82.2 GiB**. Note the *user
data volume* is `/System/Volumes/Data` (810G used per `df -H`), not `/`
(reports a nearly-empty 18G — that's the read-only System volume; the
CLAUDE.md floor methodology and `disk_snapshot.sh`'s own `df -k "$target"`
already target Data, but it's easy to check plain `df -H /` by habit and get
a wildly wrong number).

## Reusable pattern

A launchd plist that "exists on disk" is not evidence it's loaded or valid.
Before trusting any launchd-job-dependent tool output (staleness gates,
history tools, anything reading a ledger/state file a job is supposed to
maintain), verify with `launchctl list | grep <label>` AND `plutil -lint
<plist>` — file presence and file validity are two separate failure modes,
and validity failures are completely silent in launchd (no crash log, no
`launchctl list` entry at all).

See also [[feedback_2026-07-15_verify_disk_accounting_sums_before_claiming]],
[[feedback_2026-08-21_consult_memory_before_live_probes]].

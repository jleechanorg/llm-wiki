---
name: level-up-diamond-state-bug-class-2026-06-08
description: "Level-up \"diamond state\" bug class — same finish-commit pattern reproducing on production campaigns (mppfHseT 14→15, vNU3AAXHd 17→18) for months despite 90 PRs. Root cause: every PR targets ONE field; bug spans 4. Action plan: 30-LOC invariant gate + daily production observer."
metadata: 
  node_type: memory
  type: project
  originSessionId: 587748e4-1a5e-4699-bff2-28948fdd3b9f
---

# Level-up "diamond state" bug class — the months-of-failed-fixes root cause

## Bug class signature

A "diamond state" is when a level-up finish commit writes `pcd.level = N+1` atomically, but the top-level `level_up_signal: {current_level: N, target_level: N+1}` (or one of `level_up_pending` / `level_up_in_progress` / `rewards_pending.level_up_available`) is NOT cleared atomically. The `custom_campaign_state` copy IS cleared. Result: a "diamond" where pcd is committed but the signal is dangling-stale, and modal-reopen logic that reads the top-level signal misfires.

## Why: every PR targets ONE field, the bug spans FOUR

PR audit (2026-06-08) of 90 level-up PRs in 60 days:
- `level_up_pending`: 3 PRs (#7156, #7247, #7262) — all separate mechanisms (prompt, detection, router)
- `level_up_in_progress`: 1 PR (#7357) — CHANGES_REQUESTED
- `level_up_complete`: 1 PR (#7156 alone)
- `rewards_pending.level_up_available`: 1 PR (#7337) — CLOSED unmerged
- `level_up_signal` (the primary canonical signal, target_level>current_level): **NO PR promotes it to single source of truth** — only preservation fixes exist
- The "diamond" requires signal ∧ pending ∧ in_progress ∧ complete to all clear together. No PR clears all four atomically.
- The meta-fix #7268 (+5477/-2382, the largest diff in the stack) has been OPEN since 2026-06-05 with `reviewDecision=empty`. Not reviewable at 7,859 net LOC.

## Production evidence (live Firestore, owner `vnLp2G3m21PJL6kxcuAqmWSOtm73`)

- **vNU3AAXHd9N7adqWSM2p** (Vespera Thul, level 18 turn 210) — pcd.level=18, XP 266,750/305,000 (correct L18 threshold), `custom.level_up_complete=true`, but top-level `level_up_signal = {current_level:17, target_level:18}` STALE. Repro at scenes 355-358 (level_up_now → finish_level_up_return_to_game). Filed as comment on issue #7362.
- **mppfHseT9cy44Ywro4oJ** (Bg3 farming, level 15) — case study 14→15 case, finish commit limbo. State is now CLEAN, but the bug class is alive. Issue #7360, bead rev-d3gqg.

## Action plan (companion beads)

- **rev-254ez** [ACTION 1, P1] 30-LOC invariant gate in `mvp_site/rewards_engine.py`. `level_up_signal = (target > current)` is canonical. If any of {pending, in_progress, complete, rewards_pending.level_up_available} is true while signal says no level-up active, FAIL the write (DiamondStateError, do not silent-overwrite). Catches the bug CLASS, not the instance. Does not require #7268 to merge. ZFC compliant.
- **rev-544i4** [ACTION 2, P2] Daily production observer (`mvp_site/scripts/level_up_state_observer.py`) that scans jleechan campaigns and alerts on diamond state within 24h. Defense in depth: prevention for future writes, detection for current state. Wire to existing GCP test job from #7194.
- **rev-9f200** [META, P0] the meta-issue bead. Central diagnosis, PR audit, field-coverage map, root cause. Sub-beads for each new campaign repro.

## Open issues cross-linked

- #7362 — vNU3 repro (my scene-355-358 trace comment added)
- #7360 — mppfHseT 14→15 case study (bead rev-d3gqg)
- #7361 — finish-commit reliability (proposed PR-scope issue)
- #7334 — missing level-up choice (related symptom)
- #7227 — design issue to replace boolean flags with model-owned `level_up_signal`
- #7234, #7239, #7268, #7357 — open PRs (each targets a different field)

## Why the "supersedes" anti-pattern is the process signal

#7178 "replaces" #7175, #7239 "supersedes" #7155+#7235 — both predecessors remain OPEN. 8-agent supersession cycles cost ~6 reviewer-hours each per #7357's CHANGES_REQUESTED being the 3rd review of the same router change. Mandate: if title contains "supersedes", predecessors must close in the same commit.

## Why the ZFC pre-flight is correct here

The LLM never sets `level_up_signal` directly (banned from schema per rev-1pmyg). The diamond bug is a backend field-derivation/write-race issue, NOT a prompt issue. All prompt-only PRs (#7235, #7239, #7251, #6958) are working on the wrong layer. The ZFC pre-flight would have caught this: the failing agent never owned the decision that failed.

## Why: file bugs faster than they reproduce

Repro cost: 8+ minutes of MCP firestore reads + state inspection per campaign. Detection cost with observer: <2 minutes for 100 campaigns. The observer is the leverage — it converts per-campaign repro (slow, human-driven) to automated monitoring (fast, self-running).

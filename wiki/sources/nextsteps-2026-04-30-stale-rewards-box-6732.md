---
title: "Stale rewards_box xp_gained — Root Cause Confirmed"
type: source
tags: [worldarchitect-ai, rewards-engine, bug-fix, xp-gained]
date: 2026-04-30
source_file: nextsteps-2026-04-30-stale-rewards-box-6732.md
---

## Summary

Campaign `7IobpFpcOcibSyJ1pI5h` (Frieren v1) has a stale `rewards_box` with `xp_gained=2300` that persists across every subsequent turn. Root cause confirmed: `_canonicalize_core` in `rewards_engine.py` (line 1481-1538) has no dismissal guard for non-level-up `xp_gained`. The LLM's prose acknowledgment of the error ("State Cleanup: Deleted the erroneous 'rewards_box' object...") does NOT write to Firestore — it only appears in narrative text.

## Key Claims

- **Root cause**: `_canonicalize_core` non-level-up path (line 1481-1538) merges stale `xp_gained=2300` from `updated_game_state_dict["rewards_box"]` on every subsequent turn (line 1486-1488), normalizes it unchanged, and writes it back to Firestore
- **Why LLM acknowledgment doesn't fix it**: LLM narrative text ("State Cleanup: Deleted...") is prose only — it does not write to Firestore; `rewards_box` is only cleared through the `rewards_engine` canonicalization path
- **PR #6719 not responsible**: PR #6719's guard only handles `level_up_available` flag, not `xp_gained`
- **Existing dismissal for `level_up_available`**: `_canonicalize_core` has a SIM102 block (lines 1499-1506) that clears stale `level_up_available` — but no equivalent for `xp_gained`
- **Two fix approaches exist**: Display-layer scrub (PR #6733 — CONFLICTING, CHANGES_REQUESTED) vs. root-cause fix in `_canonicalize_core` (not yet implemented)

## Key Quotes

> `_canonicalize_core` has no dismissal guard for stale non-level-up `xp_gained`. When a user takes a subsequent turn without a new XP award, the stale `xp_gained=2300` from the previous turn is picked up from `updated_game_state_dict["rewards_box"]`, normalized unchanged, and written back to Firestore. — nextsteps-2026-04-30

> The LLM's narrative acknowledgment ("State Cleanup: Deleted...") is prose only — it does NOT write to Firestore. — nextsteps-2026-04-30

## Connections

- [[RewardsEngineArchitecture]] — `_canonicalize_core` is the single convergence point for all rewards canonicalization
- [[RewardsBoxDismissal]] — concept: XP-progress rewards box has no dismissal mechanism
- [[Level-Up-Signal-Dismissal-Gap]] — related gap: `level_up_available` has dismissal guard but `xp_gained` does not
- [[Normalization-Atomicity]] — `_enforce_atomicity` enforces paired None return but doesn't clear stale `xp_gained`
- [[PR #6733]] — display-layer fix attempt for this same bug (CONFLICTING)
